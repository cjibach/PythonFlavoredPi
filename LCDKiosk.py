#!/usr/bin/env python
#
# This script currently has very basic use of the Pi's Adafruit LCD Plate.  See
# the LCDutil.py script for example code that does other things, like reading
# and responding to button presses.
#
# You'll need to make sure you have the Adafruit Python library, which you can
# retrieve via git:
#    git clone https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git
#
# Once you have that, you'll need to tell Python where to find it; specifically,
# where to find the Adafruit_CharLCDPlate module, with something like this (fix
# the path to match where you cloned it):
#    PYTHONPATH=/home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCDPlate LCDKiosk.py
#
# The script will put the Pi's IP on the LCD when it starts, for convenience (note
# that this requires the Pi to have internet connectivity... need to find a better
# way to get the IP even when it doesn't).

from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate as LCD
from wsgiref.simple_server import make_server
from cgi import escape, parse_qs
from sys import argv, stdin
import socket

html = """
<html>
  <head>
    <title>LCD Kiosk Mission Control</title>
  </head>
  <body>
    <h2>LCD Kiosk Mission Control</h2>
    <form method="POST" action="LCDKiosk.wsgi">
      <table border="1">
{}
        <tr>
          <td colspan="2" align="center">
            <input type="submit" value="Send"/>
          </td>
        </tr>
      </table>
    </form>
  </body>
</html>
"""

row = """
        <tr>
          <td align="right"><b>{}:</b></td>
          <td><input type="text" name="{}"/></td>
        </tr>
"""

def namize(n):
	return n.lower().translate(None, " ")

fields = [ "Question", "Answer 1", "Answer 2", "Answer 3", "Answer 4" ]
rows = "".join([ row.format(f, namize(f)) for f in fields ])

class LCDKiosk():
	def __init__(self, ask, dev = None):
		self.ask = ask
		self.dev = dev

	def __call__(self, environ, start_response):
		ct_html = ('Content-Type', 'text/html')
		ct_text = ('Content-Type', 'text/plain')
		if environ['REQUEST_METHOD'] == 'GET':
			start_response('200 OK', [ ct_html ])
			return [ html.format(rows) ]

		elif environ['REQUEST_METHOD'] == 'POST':
			try:
				request_body_size = int(environ.get('CONTENT_LENGTH', 0))
			except (ValueError):
				request_body_size = 0
			request_body = environ['wsgi.input'].read(request_body_size)
			d = parse_qs(request_body)
			data = [ [ f, escape(d.get(namize(f), [''])[0]) ] for f in fields ]
			start_response('200 OK', [ ct_text ])
			return [ str(self.ask(data, self.dev)) ]

		start_response('404 Not found', [])

def ask_debug(q_and_a, dev = None):
	return "\n".join([ " = ".join(p) for p in q_and_a ])

def ask_console(q_and_a, dev = None):
	r = 0
	print "Question: {}".format(q_and_a[0][1])
	opts = { i : q_and_a[i][1] for i in range(1, len(q_and_a)) if len(q_and_a[i][1]) > 0 }
	for i in opts:
		print "{}: {}".format(i, opts[i])
	if len(opts) > 0:
		k = opts.keys()
		p = "Enter choice ({}): ".format(", ".join(map(str, k)))
		while r not in k:
			print p,
			try:
				r = int(stdin.readline())
			except (ValueError):
				pass
	return r

def ask_lcd(q_and_a, dev = None): # FIXME
	dev.clear()
	dev.message(q_and_a[0][1])
	dev.backlight(dev.ON)
	return 0

def main():
	lcd = None
	ask = ask_console
	try_lcd = True
	show_ip = True

	for a in argv:
		if a == "-c":
			try_lcd = False
		elif a == "-i":
			show_ip = False

	if try_lcd:
		try:
			lcd = LCD()
			ask = ask_lcd
			if show_ip: # Display IP, for headless operation
				ip = "127.0.0.1"
				try:
					s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
					s.connect(("8.8.8.8", 80))
					ip = s.getsockname()[0]
					s.close()
				except:
					pass
				lcd.message(ip)
				lcd.backlight(lcd.ON)
		except:
			pass

	try:
		server = make_server('', 8080, LCDKiosk(ask, lcd)) #ask_debug
		sa = server.socket.getsockname()
		print 'LCD Kiosk started on', sa[0], ':', sa[1]
		server.serve_forever()
	except KeyboardInterrupt:
		print 'Shutting down server'
		server.socket.close()
		if lcd != None:
			lcd.clear()
			lcd.backlight(lcd.OFF)

if __name__ == '__main__':
	main()
