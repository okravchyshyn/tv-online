#!/usr/bin/env python

import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import urlparse
import httplib

fileName =  './player.html'

#Create custom HTTPRequestHandler class
class KodeFunHTTPRequestHandler(BaseHTTPRequestHandler):
    
    #handle GET command
    def do_GET(self):
	print 'get request'
        global fileName
        fn = fileName  #file location
        try:
            #if self.path.endswith('.html'):
	    contentType = "text-html" 
	    if '?' in self.path:
		url, args = self.path.split('?')
		qs = urlparse.parse_qs(args)
		print url, args
		print qs
		KEYWORD = "channel"
		if KEYWORD in qs:
			channel_url = qs[KEYWORD]
			print channel_url
			url_container = urlparse.urlparse(channel_url[0])
			print "url_container =", url_container
			conn = httplib.HTTPConnection(url_container.netloc)
			conn.request("GET",url_container.path)
			res = conn.getresponse()
			print res.status, res.reason
			data = res.read()
			print data
			conn.close()

                	self.send_response(200)
                	self.send_header('Content-type',contentType)
                	self.end_headers()
                	self.wfile.write(data)
			return
	   
            if len(self.path) == 0:
		pass
	    elif self.path.endswith(".js"): 
	        fn = self.path[1:]
                contentType = "application/x-javascript"
            elif self.path.endswith(".swf"):
	        fn = self.path[1:]
                contentType = "application/x-javascript"
            elif self.path.endswith(".html"):
	        fn = self.path[1:]
                contentType = "text-html"
            
	    print "fileName =", fn
            if True:
                f = open(fn) #open requested file

                #send code 200 response
                self.send_response(200)

                #send header first
                self.send_header('Content-type',contentType)
                self.end_headers()

                #send file content to client
                self.wfile.write(f.read())
                f.close()
                return
            
        except IOError:
            self.send_error(404, 'file not found')
    
def run():
    print('http server is starting...')

    #ip and port of servr
    #by default http server port is 80
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, KodeFunHTTPRequestHandler)
    print('http server is running...')
    httpd.serve_forever()

if __name__ == '__main__':
    global fileName
    print sys.argv
    if len(sys.argv) > 1:
	fileName = sys.argv[1]
    run()

