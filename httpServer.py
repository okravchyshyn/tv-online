#!/usr/bin/env python

import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import urlparse
import httplib
import formPlayList as pl
#import logging
import syslog

fileName =  './player2.html'


#Create custom HTTPRequestHandler class
class KodeFunHTTPRequestHandler(BaseHTTPRequestHandler):
    
    #handle GET command
    def do_GET(self):
	print 'get request'
        syslog.syslog(syslog.LOG_INFO, 'Get request')
        global fileName
        fn = fileName  #file location
        try:
            print "PATH: ", self.path
            syslog.syslog(syslog.LOG_INFO, 'PATH' + self.path)
            #if self.path.endswith('.html'):
	    contentType = "text-html" 
	    if '?' in self.path:
		url, args = self.path.split('?')
                syslog.syslog(syslog.LOG_INFO, 'URL&PATH=' + url + ' ' + args)
		qs = urlparse.parse_qs(args)
		#print url, args
                syslog.syslog(syslog.LOG_INFO, str(qs))
		#print qs
		KEYWORD = "channel"
		if KEYWORD in qs:
                        syslog.syslog(syslog.LOG_INFO, 'I am here')
			channel_url = qs[KEYWORD][0]
                        syslog.syslog(syslog.LOG_INFO, 'channel_url=' + channel_url)
                        data = pl.httpGetRequest(channel_url)

                	self.send_response(200)
                	self.send_header('Content-type',contentType)
                	self.send_header('Access-Control-Allow-Origin','*')
                	self.end_headers()
                	self.wfile.write(data)
			return
                else:
                        syslog.syslog(syslog.LOG_INFO, 'No keyword')
	   
            if len(self.path) == 0:
		pass
            elif self.path == "/channels":
                syslog.syslog(syslog.LOG_INFO, 'Start forming playlist' )
                pass
                xml = pl.getPlayList()              
                contentType = "text-xml"
                self.send_response(200)
                self.send_header('Content-type',contentType)
                self.end_headers()
                self.wfile.write(xml)
                print "!!! XML"
                syslog.syslog(syslog.LOG_INFO, 'Playlist formed' )
                return 
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
            syslog.syslog(syslog.LOG_ERR, 'IOError 404 file not found' )
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
    syslog.syslog('Server started')
    global fileName
    print sys.argv
    if len(sys.argv) > 1:
	fileName = sys.argv[1]
    run()

