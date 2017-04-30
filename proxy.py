#!/usr/bin/env python
# coding: utf-8

import SimpleHTTPServer
import SocketServer

PORT = 8001


class Proxy(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):  # NOQA
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write('OK')


class ReusableTCPServer(SocketServer.TCPServer):
    allow_reuse_address = True

server = ReusableTCPServer(("", PORT), Proxy)

print "serving at port", PORT
server.serve_forever()
