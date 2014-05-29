import json
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
from lxml import etree
import formPlayList as fpl
import re


class EmbedHTMLParser(HTMLParser):

    anchorCounter = 0
    parentXmlEl = None


    def __init__(self, parentXmlEl):
        HTMLParser.__init__(self)
        self.parentXmlEl = parentXmlEl

    def getRelResource(self, str):
        patter = "\{parent_id[^0-9]*(\d{1,10})\}"
        r = re.search(pattern, str) 
        

    def createFolderTag(self, attrs):
        ch = etree.SubElement(self.parentXmlEl, "item")
        directory = etree.SubElement(ch, "dir")
        directory.text = "1"
        for attr in attrs:
            if attr[0] == "rel"
                pass
            print attr
 
    def createFileTag(self, attrs):
        pass

    def handle_starttag(self, tag, attrs):
        if tag == 'a'
            self.anchorCounter = self.anchorCounter + 1
            for attr in attrs:
                if attr[0] == "name" or  attr[0] == 'id':
                    if attr[1][0:2] == "fl":
                         pass
                    elif attr[1][0:2] == "dl":
                         pass
          
    def handle_endtag(self, tag):
        if tag == 'a'
            self.anchorCounter = self.anchorCounter - 1
            if self.anchorCounter == 0:
                pass
                print "Do something"
        print "End tag  :", tag


    def handle_data(self, data):
        if self.anchorCounter:
            pass

        print "Data     :", data

def buildPlayListForResource(resUrl, folderNumber, elem):
    request = url + "?ajax&folder=" + folderNumber
    print request
    response = fpl.httpGetRequest(request)
    print "Response:\n", response



if __name__ == '__main__':
    root = etree.Element("channels")

    s = "http://brb.to/video/serials/i3THZbby4d3sY3znFnxeOAg-dva-s-polovinoj-cheloveka.html"
    pl = buildPlayListForResource(s)

    #playList = getPlayList()

