import time
import xbmc
 
if __name__ == '__main__':
    monitor = xbmc.Monitor()

    with GPIOPin(3) as pin: #Pin 3 sseems to be good.
	    while True:
	        # Sleep/wait for abort for 1 second
	        if monitor.waitForAbort(1):
	            # Abort was requested while waiting. We should exit
	            break
	        if pin.value():
	        	# Initiate shutdown.
	        	xbmc.executebuiltin("ShutDown")

	        xbmc.log("hello addon! %s" % time.time(), level=xbmc.LOGDEBUG)

class GPIOPin:
	def __init__(self, pin):
		self.pin = pin

	def __enter__(self):
		xbmc.executebuiltin('System.ExecWait', 'echo "' + self.pin + '" > /sys/class/gpio/export')
		xbmc.executebuiltin('System.ExecWait', 'echo "in" > /sys/class/gpio/gpio' + self.pin + '/direction')

	def value():
		value = open('/sys/class/gpio/gpio' + self.pin + '/value', 'r').read()
		return value != '0' and value != ''

	def __exit__(self, type, value, traceback):
		xbmc.executebuiltin('System.ExecWait', 'echo "' + self.pin + '" > /sys/class/gpio/unexport')	


# http://www.raspberrypi.org/forums/viewtopic.php?f=26&t=27830
# http://elinux.org/RPi_Low-level_peripherals
# http://openelec.tv/forum/124-raspberry-pi/70693-gpio-pins-in-use
# http://kodi.wiki/view/List_of_Built_In_Functions
# http://raspberrypi.stackexchange.com/questions/19718/will-pulling-pin-5-low-will-make-the-pi-boot-up-again/19754#19754