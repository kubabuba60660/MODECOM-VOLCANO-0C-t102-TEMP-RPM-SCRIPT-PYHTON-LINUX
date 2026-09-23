# MODECOM-VOLCANO-0C-t102-TEMP-RPM-SCRIPT-PYHTON-LINUX
since the orgiginal volcano 0C does not work on linux i created a pythonm script to make it display the temperature and rpm (it works on the t102 bit idk about others)
you'll need to (at least in gigabyte motheboards idk about others) type in before turning on the script:
sudo modprobe it87 force_id=0x8628
and then:
sudo nano /etc/modprobe.d/it87.conf

and then just try to add the script to autostart i dont remember how i did that sorry
