#!/bin/bash
set -e
# This script should only be run on Ubuntu or Debian with 32-bit kernel

[ "$(whoami)" != "root" ] && exec sudo -- "$0" "$@"
if [ -z "$SUDO_USER" ]; then
  echo "Run this script with sudo, not as root"
  exit 1
fi

DISTRO=$(lsb_release -i | cut -d: -f2 | sed s/'^\t'//)
MACHINE=$(uname -m)
TARFILE="$1"

if [ "$DISTRO" != "Ubuntu" ] && [ "$DISTRO" != "Debian" ]; then
  echo "This script expects Ubuntu or Debian!"
  exit 1
#elif [ "$MACHINE" != "i686" ]; then
#  echo "This script expects a 32-bit kernel!"
#  exit 1
elif [ ! -e "$TARFILE" ]; then
  echo "File \"$TARFILE\" doesn't exist!"
  exit 1
fi

USER_HOME=$(eval echo ~${SUDO_USER})

PACKAGES="python-pip python-all-dev python-tk python-pybiggles python-pygame \
python-opengl python-pil python-pmw python-imaging-tk python-comedilib \
libcomedi-dev swig grace csh cpufrequtils openssh-server samba"

apt update -qq
apt install ${PACKAGES} -yy

# Turn off automatic updates and update notifications on Ubuntu
if [ "$DISTRO" == "Ubuntu" ]; then
  # Turn off automatic updates
  sed -i 's/"[0-9][0-9]*"/"0"/g' /etc/apt/apt.conf.d/10periodic
  # Don't look for new OS releases
  sed -i 's/^\(Prompt=\).*/\1never/' /etc/update-manager/release-upgrades
  # Turn off update notifications
  gconftool -s --type bool /apps/update-notifier/auto_launch false
  gconftool -s --type bool /apps/update-notifier/no_show_notifications true
  gconftool -s --type int /apps/update-notifier/regular_auto_launch_interval 2147483647
fi

# Make all cores use the performance governor (max frequency all the time)
##NCORES=$(getconf _NPROCESSORS_ONLN)
##for ((i=0;i<$NCORES;i++)); do cpufreq-set -c $i -r -g performance; done #do this in manual. TN: Segmentation fault happened and ignored.
# set as the default for persistence between reboots
echo 'GOVERNOR="performance"' | sudo tee /etc/default/cpufrequtils

# Ubuntu will override the "performance" setting with "ondemand"
# this will disable that service
if [ "$DISTRO" == "Ubuntu" ]; then
  update-rc.d ondemand disable
fi

# Install a samba share so the backup scripts running on the
# Plexon machines can backup the pype computer
# only do it for the shapelab user
if [ "$SUDO_USER" == "shapelab" ]; then
  (echo 'mel&co'; echo 'mel&co') | smbpasswd -a -s $SUDO_USER
  SMB_CONF=/etc/samba/smb.conf

  # Append the following to the smb.conf (if we haven't already)
  if ! grep -q "^\[$SUDO_USER\]" "$SMB_CONF"; then
    # share doesn't exist, go ahead
    cp "$SMB_CONF" "$SMB_CONF".$(date +%Y%m%d_%H%M%S).bak
    cat >> "$SMB_CONF" <<EOF
[$SUDO_USER]
   path = /home/$SUDO_USER
   guest ok = yes
   read only = no
EOF
  /usr/sbin/service smbd restart
  # This share now lives at \\IP_ADDRESS\shapelab
  fi
fi

# Extract to a scratch directory and clean up when we exit
tempdir=$(mktemp -d -p /tmp pypeinst.XXXXXXXX)
function cleanup {
  rm -rf "$tempdir"
}
trap cleanup EXIT

# Extract the source code from the archive
tar -C "$tempdir" -xzf "$TARFILE" --strip-components=1
pushd "$tempdir"

# Install Numeric and copy the headers
pushd External
tar -xzf Numeric-24.2.tar.gz
pushd Numeric-24.2
python2 setup.py install
cp -r Include/Numeric $(ls -d /usr/include/python2.[0-9] | sort | tail -1)
popd
popd

# build and install pype
PYPEDIR=/usr/local/pype2 ./build install wrapper clean
popd

# Be helpful and make the .pyperc folder if needed
mkdir -p "$USER_HOME"/.pyperc/_none
chown -R "$SUDO_USER":"$SUDO_USER" "$USER_HOME"/.pyperc
ps -ax | grep pype
echo
echo "Make sure to define PYPEDIR and any other pype-related environment"
echo "variables in your .bashrc file!"
echo
