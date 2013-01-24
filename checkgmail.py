import urllib2,base64             # For BasicHTTPAuthentication
import feedparser         # For parsing the feed
from textwrap import wrap # For pretty printing assistance

_URL = "https://mail.google.com/gmail/feed/atom"

def auth(username, password):
	request = urllib2.Request(_URL)
	astring = base64.encodestring('%s:%s' % (username,password)).replace('\n','')
	request.add_header("Authorization","Basic %s" % astring)
	return urllib2.urlopen(request)

def fill(text, width):
    '''A custom method to assist in pretty printing'''
    if len(text) < width:
        return text + ' '*(width-len(text))
    else:
        return text

def readmail(feed):
    '''Parse the Atom feed and print a summary'''
    atom = feedparser.parse(feed)
    print ""
    print atom.feed.title
    print "You have %s new mails" % len(atom.entries)
    # Mostly pretty printing magic
    print "+"+("-"*84)+"+"
    print "| Sl.|"+" Subject"+' '*48+"|"+" Author"+' '*15+"|"
    print "+"+("-"*84)+"+"
    for i in xrange(len(atom.entries)):
        print "| %s| %s| %s|" % (
            fill(str(i), 3),
            fill(wrap(atom.entries[i].title, 50)[0]+"[...]", 55),
            fill(wrap(atom.entries[i].author, 15)[0]+"[...]", 21))
    print "+"+("-"*84)+"+"

def unreadcount(u,p):
	return len(feedparser.parse(auth(u,p)).entries)

if __name__ == "__main__":
    f = auth("cgs2835","springwebweb")  # Do auth and then get the feed
    readmail(f) # Let the feed be chewed by feedparser
