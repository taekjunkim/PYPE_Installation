# Pype 2 installation guide for 64bit Linux Machine
--	Tested under Ubuntu 16.04 64bit 


## 1. Download Ubuntu 16.04 64bit desktop image, and install
http://releases.ubuntu.com/16.04/  
Install available system update

## 2. Install Nvidia driver
Remove old version of Nvidia if your graphic is supported  
$ sudo apt-get purge nvidia*  
First, add the ppa:graphics-drivers/ppa repository into the system  
$ sudo add-apt-repository ppa:graphics-drivers/ppa  
$ sudo apt update  
Next, identify your graphic card model and recommended driver:  
$ ubuntu-drivers devices  
    ### Following is an example output  
    == /sys/devices/pci0000:00/0000:00:01.0/0000:01:00.0 ==  
    modalias : pci:v000010DEd00001C03sv00001043sd000085ABbc03sc00i00  
    vendor   : NVIDIA Corporation  
    model    : GP106 [GeForce GTX 1060 6GB]  
    driver   : nvidia-driver-390 - third-party free  
    driver   : nvidia-driver-410 - third-party free recommended  
    driver   : nvidia-driver-396 - third-party free  
    driver   : xserver-xorg-video-nouveau - distro free builtin  
    - Install all recommended drivers automatically:  
    $ sudo ubuntu-drivers autoinstall  
    - Or selectively using the apt command  
    ### nvidia-410, nvidia-390,....   
    $ sudo apt install nvidia-410  
    - Reboot the system  
    $ sudo reboot  

## 3. Add eyelink repository and install dev kit
$ sudo sh ./eyelink-install.sh

## 4. Install eth32 dev kit
-	Original source of ETH32 API 
https://www.winford.com/products/eth32-downloads.php
-	Unzip the file → move to linux directory → Install
$ cd eth32api-2.01/linux
$ make
$ sudo sh ./install.sh
$ cd ~

## 5. Install libezV24 (needed for access to serial port):
-	Original source of “fixed-libezV24-0.1.3.tar.gz”
https://github.com/mazerj/pype3/tree/master/Notes
$ sudo sh ./ez-install.sh

## 6. Install pype packages
-	64bit_Pype_2019-05-18-working-copy.tar.gz is not compatible with 32 bit ubuntu
-	Several source files related to dacq3 were changed 
$ chmod +x build_install_pype_shapelab_64bit.sh
$ ./build_install_pype_shapelab_64bit.sh 64bit_Pype_2019-05-18-working-copy.tar.gz

## 7. Define PYPEDIR and other pype-specific environment variables in ~/.bashrc
$ sudo gedit ~/.bashrc
-	Add the following lines at the end of the .bashrc file
export PYPEDIR = /usr/local/pype2
export PATH = $PYPEDIR/bin:$PYPEDIR/p2m:$PATH 

## 8. Copy and paste Config.rig#-pype file and task files in the .pyperc folder
-	Make sure that the Config file has the same name as the computer
-	Make sure that display params are correct. 
-	Check ip address for Eyelink, and change it if needed
: in a new version of Eyelink, ip address was preset at 100.1.1.1

## 9. After you set the IP address (e.g., 172.16.0.103), you will try to ssh from pype controller. 
-	In new machines, ssh -X 172.16.0.103 may show you the following error message
-	No matchine cipher found: client blowfish-cbc,arcfour server ???????????????
-	blowfish-cbc,archfour are ciphers that are disabled by default for security reasons
-	You can enable them through the following steps
$ ssh -Q cipher: This will show the available cipher in the machine
$ cd /etc/ssh/
$ sudo gedit sshd_lconfig
Then type the following lines at the top of the text file
## enabled all available ciphers. Your name, Date of change
Ciphers 3des-cbc,blowfish-cbc,arcfour,... (all available ciphers from ssh-Q cipher)

### IP settings ###
Router: 172.16.0.1     Pype controller: 172.16.0.102     Pype machine: 172.16.0.103
Eth32 box: 172.16.0.104
