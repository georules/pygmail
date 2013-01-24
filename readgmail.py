#!/usr/bin/env python

def gmaildata():
	from checkgmail import unreadcount
	import ConfigParser,string,os
	config = ConfigParser.ConfigParser()
	cfile = os.path.join(os.getcwd(),"accounts")
	config.read(cfile)
	data = {}
	for section in config.sections():
		data[section] = unreadcount(config.get(section,"username"),config.get(section,"password"))
	return data
