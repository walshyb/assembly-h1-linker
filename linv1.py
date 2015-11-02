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

P_table = [PTYPE()] * P_TABLE_SIZE
E_table = [ETYPE()] * E_TABLE_SIZE
R_table = [RTYPE()] * R_TABLE_SIZE

P_tablex = R_tablex = E_tablex = ssize = filesize = textsize = E_tablexstart = R_tablexstart = ofopen = startadd = module_address = 0
gots = False
saves = ''
ifilename = ''

def ierror():
	print("Input file " + str(ifilename) + " is not linkable\n")
	sys.exit()

def processfile():
	firstchar = fptr = endptr = ''
	i = address = ''
	
	#endptr = file_buffer + filesize;
	while True:
		firstchar = fptr
		fptr += 1
		
		if firstchar == 'T':
			textsize = endptr - fptr
			if (textsize/2) > MACSIZE - module_address:
				print("ERROR: Linked program too big")
				sys.exit()
			
			#memcpy(&text_buffer[module_address], fptr, textsize);
			
			module_address += textsize/2
			break
		
		if firstchar != 'S' and firstchar != 's' and firstchar != 'P' and firstchar != 'E' and firstchar != 'R':
			ierror()
		else:
			address = fptr
			fptr = fptr + 2
			
			if fptr > endptr:
				ierror()
			
			if firstchar == 'S' or firstchar == 's':
				if(gots):
					print("ERROR: More than one starting add")
					sys.exit()
				gots = True
				saves = firstchar
				
				if firstchar == 'S':
					startadd = address
				else:
					startadd = address + module_address
				continue
			
			if firstchar == 'P':
				if P_tablex >= P_TABLE_SIZE:
					print("ERROR: P table overflow")
					sys.exit();
             
				P_table[P_tablex].address = module_address + address;
			else:
				if firstchar == 'E':
					if E_tablex >= E_TABLE_SIZE:
						print("ERROR: E table overflow")
						sys.exit();
             
					E_table[E_tablex].address = module_address + address;
				else:
					if firstchar == 'R':
						if R_tablex >= R_TABLE_SIZE:
							print("ERROR: R table overflow")
							sys.exit();
             
						R_table[R_tablex].module_address = module_address
						R_table[R_tablex].address = module_address + address
						R_tablex += 1
						continue
			
			ssize = len(fptr) + 1
			
			if firstchar == 'P':
				for i in range (0, P_tablex):
					if fptr == P_tablex[i].symptr:
						print("ERROR: Duplicate PUBLIC symbol" + fptr)
						sys.exit()
				P_table[P_tablex].symptr = fptr
				P_tablex += 1
			else:
				E_table[E_tablex].symptr = fptr
			
			fptr = fptr + len(fptr) + 1
			continue
		
		return
	
def doifile():
	pcat = ''
	global ifilename 

	if not(ifilename.endswith('.mob')):
		ifilename = ifilename + '.mob' 
	
	print ifilename
	 
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
	
	filesize = in_stream.read(FILE_BUF_SIZE)
	in_stream.close()
	
	if filesize == FILE_BUF_SIZE:
		print("Input file" + ifilename + "is too big")
		sys.exit()
	
	processfile()
	
def main():
	global ifilename
	print("Brandon Walsh")
	
	if len(sys.argv) < 3:
		print("ERROR: Incorrect number of command line args")
		sys.exit()
	print(sys.argv[0])
	
	for argx in range (1, len(sys.argv)):
		
		ifilename = sys.argv[argx]
		doifile()
	
main()