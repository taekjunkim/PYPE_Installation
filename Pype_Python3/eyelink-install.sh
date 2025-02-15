#!/bin/sh

# this sets the system up to use SR's software repository for linux
# and installs the latest versions of the required libraries.

if [ `whoami` != root ]; then
    echo "run as root!"
    exit 1
fi

# run as root..

cat <<EOF >/etc/apt/sources.list.d/eyelink.list
# Eyelink repository
deb http://download.sr-support.com/software SRResearch main
EOF

cd /tmp
# 12-2-2021 updated URL to new public key URL
wget https://download.sr-support.com/SRResearch_key
apt-key add SRResearch_key
rm SRResearch_key

apt-get update
apt-get install eyelinkcore eyelinkcoregraphics
apt-get install -f
