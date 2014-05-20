#import gdb
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import urlparse
import httplib
import re
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
from lxml import etree
import syslog


class EmbedHTMLParser(HTMLParser):
    src = None
    flashvars = None

    def handle_starttag(self, tag, attrs):
        syslog.syslog(syslog.LOG_INFO, 'has to be embed tag =' + tag)
        for attr in attrs:
            if tag == 'embed' and attr[0] == 'flashvars':
                 self.flashvars = attr[1]
                 syslog.syslog(syslog.LOG_INFO, 'flashvars =' + self.flashvars)
            if tag == 'embed' and attr[0]=='src':
                 self.src = attr[1]
                 syslog.syslog(syslog.LOG_INFO, 'src =' + self.src)
            syslog.syslog(syslog.LOG_INFO, 'attr =' + str(attr))


def extractFilePathFromEmbedBlock(embedStr):
    parser = EmbedHTMLParser()
    parser.feed(embedStr)
    if parser.flashvars is None:
        if parser.src is not None:
            url, args = parser.src.split('?')
            syslog.syslog(syslog.LOG_INFO, "split src, url=" + url + " args=" + args)
            parser.flashvars = args
        else:
            return None
    qs = urlparse.parse_qs(parser.flashvars)

    f = qs['file'][0]
    s =  qs['streamer'][0]
    syslog.syslog(syslog.LOG_INFO, 's =' + s + " f=" + f)

    if s[-1] != "/":
       s = s + '/'

    return s + f



class SearchTagData(HTMLParser):
    
    searchedUrl = None
    foundTag = False
    foundText = None

    def __init__(self, searchedTag):
	self.searchedTag = searchedTag;
        HTMLParser.__init__(self);
        pass

    def handle_starttag(self, tag, attrs):
        #print "Start tag:", tag
        if tag == 'div':
            for attr in attrs:
                if attr[0] == 'id' and attr[1] == self.searchedTag:
			print "!!!! Found tag"
                        self.foundTag = True
                        txt = self.get_starttag_text()
                        syslog.syslog(syslog.LOG_INFO, 'Tag was found =' + txt)
                        #print txt
                        return
        if self.foundTag == True:
            self.foundText = self.get_starttag_text()
            #print self.foundText
            
            syslog.syslog(syslog.LOG_INFO, 'searchedTag =' + self.foundText)
            self.foundTag = False
 
    #def handle_endtag(self, tag):
    #    print "End tag  :", tag
    #def handle_data(self, data):
    #    print "Data     :", data
    #def handle_comment(self, data):
    #    print "Comment  :", data
    #def handle_entityref(self, name):
    #    c = unichr(name2codepoint[name])
    #    print "Named ent:", c
    #def handle_charref(self, name):
    #    if name.startswith('x'):
    #        c = unichr(int(name[1:], 16))
    #    else:
    #        c = unichr(int(name))
    #    print "Num ent  :", c
    #def handle_decl(self, data):
    #    print "Decl     :", data


def httpGetRequest(url):
    syslog.syslog(syslog.LOG_INFO, 'httpGetRequest=' + url )
    url_container = urlparse.urlparse(url)
    syslog.syslog(syslog.LOG_INFO, 'url_container=' + url_container.netloc + ' path = ' + url_container.path)
    conn = httplib.HTTPConnection(url_container.netloc)
    syslog.syslog(syslog.LOG_INFO, 'Connecting ...')
    conn.request("GET",url_container.path)
    syslog.syslog(syslog.LOG_INFO, 'Request ...')
    res = conn.getresponse()
    #print res.status, res.reason
    syslog.syslog(syslog.LOG_INFO, 'httpGetRequest status=' + str(res.status) + ' reason= ' + str(res.reason) )
    url_container = urlparse.urlparse(url)
    data = res.read()
    #print data
    conn.close()
    return data

def getStreamUrl(pageUrl,searchedElement):
    syslog.syslog(syslog.LOG_INFO, 'getStreamUrl=' + pageUrl )
    url = None
    html = httpGetRequest(pageUrl)
    parser = SearchTagData(searchedElement)
    parser.feed(html)
    text = parser.foundText
    syslog.syslog(syslog.LOG_INFO, 'found tag text =' + text )
    if text is not None:
        #print text
        try:
            #m = re.search('streamer=(.*\/)&', text)
            #path = m.group(1)
            #m = re.search('file=(.*)\&type', text)
            #f = m.group(1)
            #url = path + f
            url = extractFilePathFromEmbedBlock(text)
            if url is None:
                url = "None"
            syslog.syslog(syslog.LOG_INFO, 'url=' + url )
        except:
            #print "Error in reg expression:q"
            #syslog.syslog(syslog.LOG_ERR, 'Err in reg expression' )
            syslog.syslog(syslog.LOG_ERR, 'Unexpected error' )
            url = None
    return url
  
    pass

def addChannelToList(rootXml, channelName, url):
    ch = etree.SubElement(rootXml, "item")
    title = etree.SubElement(ch, "title")
    title.text = channelName
    link = etree.SubElement(ch, "link")
    #link.text = "\"" + url + "\""
    link.text =  url
    pass

def getPlayList():
    root = etree.Element("channels")

    addChannelToList(root, "1+1", "http://stream1115.tsn.ua:1935/streamlive/189931/playlist.m3u8|COMPONENT=HLS")
    
    url = getStreamUrl("http://tvx.com.ua/tv/kanal-2-plus-2/", "video-block")
    if url is not None:
        addChannelToList(root, "2+2", url)

    url = getStreamUrl("http://tvx.com.ua/tv/ictv/", "video-block")
    if url is not None:
        addChannelToList(root, "ictv", url)
    
    url = getStreamUrl("http://tvx.com.ua/tv/5-kanal/", "video-block")
    if url is not None:
        addChannelToList(root, "5 kanal", url)
 
    url = getStreamUrl("http://tvx.com.ua/tv/novy-kanal-online/", "video-block")
    if url is not None:
        addChannelToList(root, "novyy", url)
    
    url = getStreamUrl("http://tvx.com.ua/tv/kanal-stb/", "video-block")
    if url is not None:
        addChannelToList(root, "stb", url)

    #url = getStreamUrl("http://tvx.com.ua/tv/pervyj-nacionalnyj/", "video-block")
    #if url is not None:
    #    addChannelToList(root, "stb", url)
   

    syslog.syslog(syslog.LOG_INFO, 'xml=' + etree.tostring(root) )
 
    print etree.tostring(root)
    return etree.tostring(root)



if __name__ == '__main__':
  
    playList = getPlayList()

