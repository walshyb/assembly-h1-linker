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
ofilename = ''
text_buffer = [0] * (MACSIZE+1)
#text_buffer = ''
file_buffer = '' * FILE_BUF_SIZE
file = None
in_stream = None
out_stream = None

def ierror():
	print("Input file " + str(ifilename) + " is not linkable\n")
	sys.exit()
'''	
def processfile():
	global in_stream, module_address, P_table, E_table, R_table, P_tablex, E_tablex, R_tablex
	address = 0
	i = 1
	while True:
		firstchar = in_stream.read(i)
		i = i +1
		print "here" + firstchar
		
		if firstchar == 'T':
			textsize = len(file.read())
			if textsize/2 > MACSIZE - module_address:
				print("ERROR: Linked program too big")
				sys.exit()
			
			text_buffer[module_address] = textsize
			
			module_address += textsize/2
			break
	
		if firstchar != 'S' and firstchar != 's' and firstchar != 'P' and firstchar != 'E' and firstchar != 'R':
			ierror()
		else:
			address = 1
			
			if firstchar == 'S' or firstchar == 's':
				if gots:
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
	         
				P_table[P_tablex].address = module_address + address
				print module_address
				print address
			else:
				if firstchar == 'E':
					if E_tablex >= E_TABLE_SIZE:
						print("ERROR: E table overflow")
						sys.exit();
	         
					E_table[E_tablex].address = module_address + address
				else:
					if firstchar == 'R':
						if R_tablex >= R_TABLE_SIZE:
							print("ERROR: R table overflow")
							sys.exit();
	         
						R_table[R_tablex].module_address = module_address
						R_table[R_tablex].address = module_address + address
						R_tablex += 1
						continue
	
			if firstchar == 'P':
				print "in last P check"
				for j in range (0, P_tablex):
					if firstchar == P_table[j].symptr:
						print("ERROR: Duplicate PUBLIC symbol" + firstchar)
						sys.exit()
				P_table[P_tablex].symptr = firstchar
				P_tablex += 1
			else:
				E_table[E_tablex].symptr = firstchar
		return
'''
def processfile():
	global in_stream, startadd, gots, module_address, P_table, E_table, R_table, P_tablex, E_tablex, R_tablex
	
	address = 0
	
	with in_stream as file:
 		while True:
			char = file.read(1)
			#check if char (word) is P,E,R, or T
			#check if word is 2bit hex 
			if not char:
				print "End of file"
				break
			
			if char == 'T':
				print 't'
				#do stuff
			#if char != 'S' and char != 's' and char != 'P' and char != 'E' and char != 'R':
			#	ierror()
			#else:
			if char == 'S' or char == 's':
				if gots:
					print("ERROR: More than one starting add\n")
					sys.exit()
				gots = True
				saves = char
				
				if char == 'S':
					startadd = address
				else:
					startadd = address + module_address
				continue
			
			if char == ' ':
				print char.encode('hex')
			else:
				print char
	
def doifile():
	global ifilename, out_stream, ofopen, in_stream, ofilename
	
	if not(ifilename.endswith('.mob')):
		ifilename = ifilename + '.mob'
	
	
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
		ofilename = ofilename.rsplit( ".", 1 )[ 0 ]	#rid of ./mob
		ofilename = ofilename + '.mac' #add .mac
	
		if platform.system() == 'Windows':
			out_stream = open(ofilename, "wb")
		else:
			out_stream = open(ofilename, "w")
			
		if not(out_stream):
			print("ERROR: Cannot open output file" + ofilename)
			sys.exit()
	

	#if filesize == FILE_BUF_SIZE:
		#print("Input file" + ifilename + "is too big")
		#sys.exit()

	processfile()

def main():
	global ifilename, out_stream, in_stream, E_tablexstart,R_tablexstart,P_tablexstart
	j = 0
	print("Brandon Walsh")
	
	
	if len(sys.argv) < 3:
		print("ERROR: Incorrect number of command line args")
		sys.exit()
		
	
	in_stream = open('testb.mob', 'r')
	processfile()
	'''
	for argx in range (1, len(sys.argv)):
		ifilename = sys.argv[argx]
		doifile()
	
	for E_tablexstart in range (E_tablexstart, E_tablex):
		j = 0
	
	while j < P_tablex and P_table[j].symptr != E_table[E_tablexstart].symptr:
		j += 1
		
		if j < P_tablex:
			text_buffer[E_table[E_tablexstart].address] = text_buffer[E_table[E_tablexstart].address] & 0xf000 | (text_buffer[E_table[E_tablexstart].address] + P_table[j].address ) & 0x0fff
		else:
			break
	
	if E_tablexstart != E_tablex:
		print("ERROR: Unresolved external symbol " + E_table[E_tablexstart].symptr)
		sys.exit()
		
	#for R_tablexstart in range (R_tablexstart, R_tablex):
		#text_buffer[R_table[R_tablexstart].address] = text_buffer[R_table[R_tablexstart].address] & 0xf000 | (text_buffer[R_table[R_tablexstart].address] + R_table[R_tablexstart].module_address) & 0x0fff
		
	for i in range (0, P_tablex):
		out_stream.write("P")
		out_stream.write(str(P_table[i].address))
		out_stream.write(P_table[i].symptr)
	
	for i in range (0, R_tablex):
		out_stream.write("R")
		out_stream.write(str(R_table[i].address))
	
	for i in range(0, E_tablex):
		out_stream.write("R")
		out_stream.write(E_table[i].address)
	
	if gots:
		out_stream.write(saves)
		out_stream.write(startadd)

	out_stream.write("T")
	
	out_stream.write(str(text_buffer))
	
	out_stream.close()

	print("here")
	'''
main()