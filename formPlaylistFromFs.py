import json
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
from lxml import etree
import formPlayList as fpl
import re
import urlparse

def getUrlSchemaAndNetloc(url):
    u = urlparse.urlparse(url)
    return u.scheme + "://" + u.netloc

class FS_UA_HTMLParser(HTMLParser):

    anchorCounter = 0
    parentXmlEl = None
    itemXmlEl = None
    thisIsDirectory = False
    resourceId = 0
    resUrl = None
    isProcessed = False

    def __init__(self, resUrl, parentXmlEl):
        HTMLParser.__init__(self)
        self.parentXmlEl = parentXmlEl
        self.resUrl = resUrl

    def getRelResource(self, str):
        pattern = "\{parent_id[^0-9]*(\d{1,10}).*\}"
        print "getRelResource=", str
        r = re.search(pattern, str) 
        if r is not None and len(r.groups()) > 0:
            print "getRelResouce=", r.group(1)
            return r.group(1)
        else:
            print "getRelResouce=None"
            return None        

    def createResourceTag(self, ifDirectory, relAttr, href):
        print "createResouceTag"
        #self.isProcessed = True
        #self.anchorCounter = self.anchorCounter + 1
        
        self.itemXmlEl = etree.SubElement(self.parentXmlEl, "item")
        directory = etree.SubElement(self.itemXmlEl, "dir")
        directory.text = str(ifDirectory)
        if relAttr is not None:
            print "createResouceTag attr=", relAttr
            #self.resourceId = res
            resource = etree.SubElement(self.itemXmlEl, "resource")
            resource.text = relAttr

        if ifDirectory == False and href is not None:
            hrefEl  = etree.SubElement(self.itemXmlEl, "href")
            hrefEl.text = href
            print "createResourceTag=", href
 
    def createFileTag(self, attrs):
        pass

    def handle_starttag(self, tag, attrs):
        print "Start tag  :", tag ," = " ,self.get_starttag_text() 
        if tag == 'a':
            foundSearchedAnchor = False
            relAttr = None
            href = None
            for attr in attrs:
                if attr[0] == "name" or  attr[0] == 'id':
                    foundSearchedAnchor = True 
                    print "dir or file:" , attr[1][0:2]
                    if attr[1][0:2] == "fl":
                         self.thisIsDirectory = True
                         #elf.createResourceTag(1, attrs)
                         #elf.createResourceTag(0, attrs)

                if attr[0] == "rel":
                    relAttr = self.getRelResource(attr[1])
                    if relAttr is not None:
                        self.resourceId = relAttr
                if attr[0] == "href":
                    href = attr[1]
                    href = getUrlSchemaAndNetloc(self.resUrl) + href
                    print "href=", href

            if foundSearchedAnchor == True:
                 self.isProcessed = True
                 self.anchorCounter = self.anchorCounter + 1
                 self.createResourceTag(self.thisIsDirectory, relAttr, href)

    def handle_endtag(self, tag):
        if tag == 'a' and self.isProcessed == True:
            self.anchorCounter = self.anchorCounter - 1
            if self.anchorCounter == 0:
               if self.thisIsDirectory == True:
                    print "Call buildPlayListForResource=", self.resourceId
                    buildPlayListForResource(self.resUrl, self.resourceId, self.itemXmlEl)
                    print "End tag  :", tag
                    self.isProcessed = False


    def handle_data(self, data):
        if (self.isProcessed == True and self.thisIsDirectory == True and 
             data is not None and len(data.strip()) > 0 ):
            title = etree.SubElement(self.itemXmlEl, "title")
            title.text = data

            print "Data     :", data

def buildPlayListForResource(resUrl, folderNumber, elem):
    request = resUrl + "?ajax&folder=" + str(folderNumber)
    print request
    response = fpl.httpGetRequest(request)
    #print "Response:\n", response
    response = response.decode("utf-8")
    parser = FS_UA_HTMLParser(resUrl, elem)
    parser.feed(response)


if __name__ == '__main__':
    root = etree.Element("channels")

    s = "http://brb.to/video/serials/i3THZbby4d3sY3znFnxeOAg-dva-s-polovinoj-cheloveka.html"
    pl = buildPlayListForResource(s, 0 ,root)
    root_str = etree.tostring(root)
    #playList = getPlayList()
    f = open('list.xml', 'w')
    f.write(root_str)
    f.close()

