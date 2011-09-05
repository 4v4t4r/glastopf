
import sys
import logging
logging.basicConfig(level=logging.DEBUG)

from evnet import loop, unloop, listenplain
from evnet.util import EventGen
from evnet.promise import Promise

import modules.HTTPUtil as HTTPUtil

# WebSocket based on Mark Schloessers evnet example.

class WebSockListener(EventGen):
	def __init__(self, host, port):
		EventGen.__init__(self)

		self.l = listenplain(host=host, port=port)
		self.l._on('connection', self.connection)

	def connection(self, c, addr):
		print 'cli', addr
		self._event('connection', WebSock(c, addr))

class WebSock(EventGen):
	def __init__(self, c, addr):
		EventGen.__init__(self)
		self.c, self.addr = c, addr
	
		self.c._on('ready', self.ready)
		self.c._on('close', self.closed)
		self.c._on('read', self.read)

	def ready(self):
		self._event('ready')

	def closed(self, e):
		self._event('close', e)

	def read(self, d):
		#print 'read', repr(d)
		Server = HTTPUtil.HTTPParser()
		parsed_request = Server.parse_request(d)
		print parsed_request.method, parsed_request.url
		self.send(HTTPUtil.HTTPServerResponse.response_header)
		self.send("abc")
		self.c.close()
		
	def send(self, s):
		self.c.write(s)

if __name__ == '__main__':
	a = WebSockListener(sys.argv[1], int(sys.argv[2]))
	print "Glastopf running on:", sys.argv[1] + ":" + sys.argv[2], "waiting for connections..."
	print ""
	
	def new_conn(c):
		def onready():
			def dbgprint(r):
				print 'dbgprint', r

		def closed(e):
			pass
			#print e

		c._on('ready', onready)
		c._on('close', closed)

	a._on('connection', new_conn)

	loop()