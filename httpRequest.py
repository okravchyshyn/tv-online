import httplib as h


conn = h.HTTPConnection("tvx.com.ua")
conn.request("GET","/tv/kanal-2-plus-2/")
res = conn.getresponse()
print res.status, res.reason
data = res.read()
print data
conn.close()



def do_GET(self):
    qs = {}
    path = self.path
    if '?' in path:
        path, tmp = path.split('?', 1)
        qs = urlparse.parse_qs(tmp)
    print path, qs

