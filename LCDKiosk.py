#!/usr/bin/env python

from SimpleHTTPServer import SimpleHTTPRequestHandler
from wsgiref.simple_server import make_server
from cgi import parse_qs, escape
from sys import stdin

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
	def __init__(self, ask):
		self.ask = ask

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
			return [ self.ask(data) ]

		start_response('404 Not found', [])

def ask_debug(q_and_a):
	return "\n".join([ " = ".join(p) for p in q_and_a ])

def ask_console(q_and_a):
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
	return str(r)

def main():
	try:
		server = make_server('127.0.0.1', 8080, LCDKiosk(ask_console)) #ask_debug
		sa = server.socket.getsockname()
		print 'LCD Kiosk started on', sa[0], ':', sa[1]
		server.serve_forever()
	except KeyboardInterrupt:
		print 'Shutting down server'
		server.socket.close()

if __name__ == '__main__':
	main()
