The following is a rough guide on how to set up a pype machine from a CLEAN
install of a Debian-based (usually Ubuntu) operating system.

From this directory execute the following commands in a shell

sudo su
chmod +x build_install_pype_shapelab.sh
./build_install_pype_shapelab.sh tarfile.tar.gz

and enter the user's sudo password. Replace tarfile.tar.gz with the appropriate
file path to a working-copy tar file.

Copy a config file to ~/.pyperc. This file should be named Config.<hostname>,
where <hostname> is the result of executing "hostname -s" in a terminal. You can
also copy over a set of tasks and place them in ~/.pyperc/Tasks.

You'll need to manually set the appropriate IP addresses for both ethernet
adapters: one for the ETH32 box and one for Eyelink. The addresses are usually
one less than the remote addresses. For example, if the ETH32 box has address
172.16.0.104, the address on the adapter connected to the ETH32 box should be
172.16.0.103. I'd suggest replicating an existing rig's setup.

You'll need to find the appropriate video driver for the installed NVIDIA card
and install it through "sudo apt-get install <driver-package-name>". The correct
package name will depend on the particular graphics card, especially if the card
is old (i.e., installing the nvidia-current package would be a bad idea since
that driver may have dropped support for your card). You can also use the
"Additional Drivers" program in Ubuntu.

You'll also need to use the cpufrequtils package to turn all of the cores to
their maximum frequency. The install script should have done this for you (and
made the setting permanent). You should check that "cpufreq-info" reports that
the "performance" governor is in use after a reboot.

The final step is configuring the display. Some video splitters/KVMs do not pass
the allowed resolution and timing modes to the video card. Because of this, you
may notice that only a small number of resolutions are available. These are the
"safe" defaults. To get more modes, you will have to modify a configuration
file.

I recommend, initially, to only plug in the subject's monitor to the video card.
Now, run the NVIDIA X Server Settings program and save an xorg.conf. This file
now contains auto-detected settings from the display. You can use the xorg.conf
in  this directory to help edit your machine's conf to unlock the modes hidden
by the  video splitter or KVM (once you plug those in). You can use the programs
gtf or cvt to generate the mode lines you see in the example xorg.conf. Keep in
mind that the subject's and experimenter's display may not support the same
mode. In that case, you will need to use a mode supported by both monitors.

There is an example xorg.conf in the same directory as this README. It is not
guaranteed to work on your machine's hardware.

Don't forget to define PYPEDIR and other pype-specific environment variables in
~/.bashrc.

Lastly, adjust the pype config file so that the values match the monitor's
current resolution and physical dimensions.
