#! /bin/bash
### script should be executed by the bash interpreter

### Exit on error: script will exit if any command returns a non-zero exit status
set -e

### check if the current user is not root user, 
### if that's true then the command "exec sudo -- "$0" "$@"" is executed, 
### this command runs the current script using "sudo" command, 
### which allows the current user to execute the script as root user.
[ "$(whoami)" != "root" ] && exec sudo -- "$0" "$@"

### If the SUDO_USER variable is empty, 
### it means the script is being run as the root user, and not through the sudo command. 
### In this case, the script will print the message "Run this script with sudo, not as root" 
### and exit with a status code of 1 (exit 1), indicating an error.
if [ -z "$SUDO_USER" ]; then
    echo "Run this script with sudo, not as root"
    exit 1
fi

### The command starts by calling lsb_release -i, 
### which retrieves information about the Linux distribution and 
### its version from the LSB (Linux Standard Base) and in this case, 
### it returns the name of the distribution.

### cut -d: -f2 is used to extract the second field (after the colon) 
### from the output of the lsb_release -i command.

### sed s/'^\t'// is used to remove any leading tabs 
### from the output of the previous command, so that only the name of the distribution is left.

### So the final output of the command is the name of the Linux distribution. 
### The variable DISTRO is storing that value.
DISTRO=$(lsb_release -i | cut -d: -f2 | sed s/'^\t'//)

### returns the machine hardware name
MACHINE=$(uname -m)

### The $1 is a special variable in bash 
### that holds the first command-line argument passed to the script.
TARFILE="$1"

### This script ensures that 
### the script is running on an Ubuntu or Debian distribution, 
### on a 64-bit machine and the passed TARFILE argument is a valid file.
if [ "$DISTRO" != "Ubuntu" ] && [ "$DISTRO" != "Debian" ]; then
    echo "This script expects Ubuntu or Debian!"
    exit 1
elif [ "$MACHINE" != "x86_64" ]; then
    echo "This script expects a 64-bit kernel!"
    exit 1
elif [ ! -e "$TARFILE" ]; then
    echo "File \"$TARFILE\" doesn't exist!"
    exit 1
fi

USER_HOME=$(eval echo ~${SUDO_USER})

### to update the package list
### The option -qq is used to suppress output, making the update process less verbose.
sudo apt update -qq

### to install the python 3.10
sudo apt install python3.10

### to install PIP
sudo apt install python3-pip

pip3 install h5py numpy PyOpengl pandas Pillow pygame scipy pmw
sudo apt-get install python3-pil.imagetk

#PACKAGES="python3-all-dev python3-comedilib python3-h5py \
#python3-numpy python3-opengl python3-pandas \
#python3-pil python3-pygame python3-scipy python3-tk \
#libcomedi-dev libcomedi0 swig grace csh \
#libsdl2-dev libsdl1.2-dev cpufrequtils openssh-server samba"

# pip3 install tk doesn't work with pype.py
PACKAGES="libcomedi-dev libcomedi0 swig grace csh python3-tk \
cpufrequtils openssh-server samba"

### the option -yy is used to automatically assume yes 
### when prompted to confirm installation or any other package configuration options.
sudo apt install ${PACKAGES} -yy

### python-dev-tools pmw
#pip3 install python-dev-tools pmw

### biggles: seems to be used in mplot.py (do we need this? and not sure if python3 supports this)
#sudo apt-get libplot-dev plotutils
#pip3 install biggles

# Turn off automatic updates and update notifications on Ubuntu
### I don't know whether the following settings are working well in recent ubuntu versions
if [ "$DISTRO" = "Ubuntu" ]; then
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
#echo 'GOVERNOR="performance"' | sudo tee /etc/default/cpufrequtils

### Ubuntu will override the "performance" setting with "ondemand"
### this will disable that service
#if [ "$DISTRO" = "Ubuntu" ]; then
#  update-rc.d ondemand disable
#fi

# Install a samba share so the backup scripts running on the
# Plexon machines can backup the pype computer
# only do it for the shapelab user
if [ "$SUDO_USER" = "shapelab" ]; then
    (echo 'mel&co'; echo 'mel&co') | smbpasswd -a -s $SUDO_USER
    SMB_CONF=/etc/samba/smb.conf

    # Append the following to the smb.conf (if we haven't already)
    if ! grep -q "^\[$SUDO_USER\]" "$SMB_CONF"; then
        # share doesn't exist, go ahead
        ### create a back-up file
        cp "$SMB_CONF" "$SMB_CONF".$(date +%Y%m%d_%H%M%S).bak

        ### append the text between EOF and EOF to the smb.conf file
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

### This script creates a temporary directory called "pypeinst" in the /tmp directory, 
### assigns its path to the variable "tempdir", and then defines a function called "cleanup" 
### which removes the directory when called. 
### The last line of the script uses the "trap" command to execute the "cleanup" function 
### when the script exits. 
### This ensures that the temporary directory is always removed even if the script is terminated prematurely.
tempdir=$(mktemp -d -p /tmp pypeinst.XXXXXXXX)
function cleanup {
    rm -rf "$tempdir"
}
trap cleanup EXIT

### uses the "tar" command to extract the contents of a tar file called "$TARFILE" 
### into the temporary directory "$tempdir". 
### The "-C" option is used to specify the destination directory, 
### and the "-xzf" options are used to extract the contents in gzip format, 
### and the "--strip-components=1" option is used to remove 
### the leading directory components of the file names in the archive.
tar -C "$tempdir" -xzf "$TARFILE" --strip-components=1

### uses the "pushd" command, which changes the current directory to "$tempdir" 
### and also pushes the current directory onto a stack 
### so it can be returned to later using the "popd" command. 
### This allows the script to operate within the context of the extracted files 
### without having to constantly reference the full path of the temporary directory.
pushd "$tempdir"

### Numeric is an old package not used anymore, replaced with numpy
### So, the following lines could be omitted. 
#--------------------------------------------------------------------------
## Install Numeric and copy the headers
#pushd External
#tar -xzf Numeric-24.2.tar.gz
#pushd Numeric-24.2
#python2 setup.py install
#cp -r Include/Numeric $(ls -d /usr/include/python2.[0-9] | sort | tail -1)
#popd
#popd
#--------------------------------------------------------------------------

# build and install pype
PYPEDIR=/usr/local/pype_python3 ./build install wrapper clean
popd

# Be helpful and make the .pyperc folder if needed
mkdir -p "$USER_HOME"/recordFiles
chown -R "$SUDO_USER":"$SUDO_USER" "$USER_HOME"/recordFiles
mkdir -p "$USER_HOME"/.pyperc/_none
chown -R "$SUDO_USER":"$SUDO_USER" "$USER_HOME"/.pyperc
ps -ax | grep pype
echo
echo "Make sure to define PYPEDIR and any other pype-related environment"
echo "variables in your .bashrc file!"
echo
