#!/usr/bin/env python

import sys
import platform

if platform.system() == 'Windows':
	fdiv = "\\"
else:
	fdiv = "/"

#------------------------------

BUF_SIZE = 121
MACSIZE = 4096
P_TABLE_SIZE = 5
E_TABLE_SIZE = 5
R_TABLE_SIZE = 5
FILE_BUF_SIZE = 12000

#------------------------------

class PTYPE:
	address = ''
	symptr = ''

class ETYPE:
	address = ''
	symptr = ''
	
class RTYPE:
	address = ''
	module_address = ''
	
#------------------------------

P_tablex = R_tablex = E_tablex = ssize = filesize = textsize = E_tablexstart = R_tablexstart = ofopen = startadd = module_address = 0
	
ifilename = ''

def ierror():
	print("Input file " + str(ifilename) + " is not linkable\n")
	sys.exit()

def processfile():
	firstchar = fptr = endptr = ''
	i = address = ''
	
	#endptr = file_buffer + filesize
	
def doifile():
	pcat = ''
	
	if not(ifilename.endswith('.mob')):
		ifilename + '.mob' 
	 
	if platform.system() == 'Windows':
		in_stream = open(ifilename, 'rb')
	else:
		in_stream = open(ifilename, 'r')
		
	if not(in_stream):
		print("ERROR: Cannot open input file" + ifilename)
    	sys.exit()

	if not(ofopen):
		ofopen = 1
		ofilename = ifilename
		ofilename.rsplit( ".", 1 )[ 0 ]	#rid of ./mob
		ofilename + '.mac' #add .mac
	
		if platform.system() == 'Windows':
			out_stream = open(ofilename, "wb")
		else:
			out_stream = open(ofilename, "w")
			
		if not(out_stream):
			print("ERROR: Cannot open output file" + ofilename)
			sys.exit()
	
	