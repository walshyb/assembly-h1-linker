#!/usr/bin/env python

#sparc: big endian
#linux: little endian
import sys
import platform

try:
  DOS
except NameError:
  try:
  	SPARC
  except NameError:
  	try:
  		LINUX
  	except NameError:
  		DOS = 1

BUF_SIZE = 121
MACSIZE = 4096
P_TABLE_SIZE = 5
E_TABLE_SIZE = 5
R_TABLE_SIZE = 5
FILE_BUF_SIZE = 12000

class PTYPE(object):
    address = None
    symptr = None

class ETYPE(object):
    address = None
    symptr = None

class RTYPE(object):
    address = None
    module_address = None

try:
	SPARC
except NameError:
	try:
		LINUX
	except NameError:
		try:
			DOS
		except NameError:
			x=1
		else:
			fdiv = '\\'
	else:
		fdiv = '/'
else:
	fdiv = '/'

print fdiv

author = "linv1 written by Brandon Walsh"
buf = [None] * BUF_SIZE
ifilename = None
ofilename = None
file_buffer = [None] * FILE_BUF_SIZE
filesize = 0

def ierror():
	print "Input file " + str(ifilename) + " is not linkable\n"
	sys.exit()

def processfile():
	endptr = file_buffer + filesize
	fptr = file_buffer

	#while(1):
		#firstchar = 

print sys.byteorder
print platform.system()