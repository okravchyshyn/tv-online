''#import gdb
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import urlparse
import httplib

from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint


class SearchTagData(HTMLParser):
    
    searchedUrl = None
    foundTag = False

    def __init__(self, searchedTag):
	self.searchedTag = searchedTag;
        HTMLParser.__init__(self);
        pass

    def handle_starttag(self, tag, attrs):
        print "Start tag:", tag
        if tag == 'div':
            for attr in attrs:
                if attr[0] == 'id' and attr[1] == self.searchedTag:
			print "!!!! Found tag"
                        self.foundTag = True
                        txt = self.get_starttag_text()
                        print txt
                        return
        if self.foundTag == True:
            txt = self.get_starttag_text()
            print txt
            for attr in attrs:
                print attr
                self.foundTag = False
 
    def handle_endtag(self, tag):
        print "End tag  :", tag
    def handle_data(self, data):
        print "Data     :", data
    def handle_comment(self, data):
        print "Comment  :", data
    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        print "Named ent:", c
    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        print "Num ent  :", c
    def handle_decl(self, data):
        print "Decl     :", data


def httpGetRequest(url):
    url_container = urlparse.urlparse(url)
    conn = httplib.HTTPConnection(url_container.netloc)
    conn.request("GET",url_container.path)
    res = conn.getresponse()
    print res.status, res.reason
    data = res.read()
    print data
    conn.close()
    return data

def getStreamUrl(pageUrl,searchedElement):
    html = httpGetRequest(pageUrl)
    parser = SearchTagData(searchedElement)
    parser.feed(html);
  
    pass

def getPlayList():
    url = getStreamUrl("http://tvx.com.ua/tv/kanal-2-plus-2/", "video-block")
    print url



if __name__ == '__main__':
    playList = getPlayList()

