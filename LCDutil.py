#!/usr/bin/python

from sys import argv
from time import sleep
#from MockPlate import Adafruit_CharLCDPlate
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

# Examine first command-line argument, if present,
# to determine which mode of execution to follow
mode = 0 # default to "help" mode
if len(argv) > 1:
	if argv[1] == "off":
		mode = 1
	elif argv[1] == "mms":
		mode = 2
	elif argv[1] == "ghn":
		mode = 3
	elif argv[1] == "msg":
		mode = 4
	elif argv[1] == "led":
		mode = 5

lcd = None
# If mode is other than "help", initialize LCD plate
if mode > 0:
	# Initialize the LCD plate.  Should auto-detect correct I2C bus.  If not,
	# pass '0' for early 256 MB Model B boards or '1' for all later versions
	lcd = Adafruit_CharLCDPlate()
else: # else, print "help" message and exit
	print "Usage: lcd command"
	print "   command = off | mms | ghn | msg 'message' [color] | led color ['message']"
	print "     color = off | red | green | blue | yellow | teal | violet | white | on"

# Define useful functions
def btnSet(btns):
	result = 128
	for b in btns:
		result += (1 << b)
	return result
def btnCheck(b):
	if b >= 128:
		c = b - 128
		return lcd.buttons() & c == c
	else:
		return lcd.buttonPressed(b)
def btnLoop(btns, quit):
	prev =  (lcd.SELECT, "", lcd.ON)
	while True:
		for b in btns:
			if btnCheck(b[0]):
				if b is not prev:
					lcd.clear()
					lcd.message(b[1])
					lcd.backlight(b[2])
					prev = b
				break
		if btnCheck(quit):
			lcd.clear()
			lcd.backlight(lcd.OFF)
			break
def setColor(color):
	colors = (("off", lcd.OFF), ("red", lcd.RED), ("green", lcd.GREEN),
	          ("blue", lcd.BLUE), ("yellow", lcd.YELLOW), ("teal", lcd.TEAL),
	          ("violet", lcd.VIOLET), ("white", lcd.WHITE), ("on", lcd.ON))
	led = lcd.OFF
	for c in colors:
		if color.lower() == c[0]:
			led = c[1]
			break
	lcd.backlight(led)

if mode == 1:
	# Clear display and shut off backlight
	lcd.clear()
	lcd.backlight(lcd.OFF)
	print "The LCD has been cleared and the backlight turned off."
elif mode == 2:
	btn = ((lcd.LEFT  , "   Melbourne\n   Makerspace", lcd.RED),
	       (lcd.RIGHT , "   Melbourne\n   Makerspace", lcd.BLUE),
	       (lcd.UP    , " Jaycon Systems", lcd.GREEN),
	       (lcd.DOWN  , "    Automate\n   Your Life!", lcd.GREEN),
	       (lcd.SELECT, "", lcd.OFF))
	btnLoop(btn, ((1 << lcd.UP) | (1 << lcd.DOWN)))
elif mode == 3:
	btn = ((btnSet((lcd.RIGHT, lcd.LEFT)), "  the meaning\n of life is 42!  ", lcd.TEAL),
	       (lcd.LEFT  , "     hello\n     world!", lcd.GREEN),
	       (lcd.RIGHT , "    goodbye\n     world!", lcd.RED),
	       (lcd.UP    , "     coding\n    is epic!", lcd.BLUE),
	       (lcd.DOWN  , "      why?\n   it just is", lcd.YELLOW),
	       (lcd.SELECT, "", lcd.OFF))
	btnLoop(btn, 128 + ((1 << lcd.UP) | (1 << lcd.DOWN)))
elif mode == 4:
	lcd.message(argv[2]) if len(argv) > 2 else lcd.clear()
	setColor(argv[3] if len(argv) > 3 else "off")
elif mode == 5:
	lcd.message(argv[3]) if len(argv) > 3 else lcd.clear()
	setColor(argv[2] if len(argv) > 2 else "off")
