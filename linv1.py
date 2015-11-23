#!/usr/bin/env python

import sys

MACSIZE = 4096
P_TABLE_SIZE = 5
E_TABLE_SIZE = 5
R_TABLE_SIZE = 5
FILE_BUF_SIZE = 12000

#------------------------------

class PTYPE:
	address = 0
	symptr = 0

class ETYPE:
	address = 0
	symptr = 0
	
class RTYPE:
	address = 0
	module_address = 0
	
#------------------------------

P_table = [PTYPE()] * P_TABLE_SIZE
E_table = [ETYPE()] * E_TABLE_SIZE
R_table = [RTYPE()] * R_TABLE_SIZE

P_tablex = R_tablex = E_tablex = filesize = textsize = E_tablexstart = R_tablexstart = ofopen = startadd = module_address = text_buffer_size = 0
gots = False
saves = ''
ifilename = ''
ofilename = ''
text_buffer = [0] * (MACSIZE+1)
file_buffer = []
file = None
in_stream = None
out_stream = None

def ierror():
	print("Input file " + str(ifilename) + " is not linkable\n")
	sys.exit()

def processfile():
	global startadd, gots, module_address, P_table, E_table, R_table, P_tablex, E_tablex, R_tablex, text_buffer_size
	i = 0
	address = 0
	endptr = file_buffer[len(file_buffer)-1]
	fptr = file_buffer[i]
	
	while True:
		firstchar = fptr
		i += 1
		fptr = file_buffer[i]

		if firstchar == 'T':
			textsize = len(file_buffer) - i

			if textsize/2 > MACSIZE - module_address:
				print("ERROR: Linked program too big")
				sys.exit()
			module_address_Save = module_address
			i_Save = i

			for j in range(i, len(file_buffer)):
				file_buffer[i] = hex(ord(file_buffer[i])).lstrip("\\x")
				file_buffer[i] = int(file_buffer[i], 16)
				
				if file_buffer[i] == 0:
					i+=1
				else:
					text_buffer[module_address] = file_buffer[i]
					i += 1
					module_address += 1
					text_buffer_size += 1

			module_address = module_address_Save
			i = i_Save
			module_address += textsize/2

			break
		
		if firstchar != 'S' and firstchar != 's' and firstchar != 'P' and firstchar != 'E' and firstchar != 'R':
			ierror()
		else:
			address = int(fptr.encode('hex'), 16)
			i += 2
			fptr = file_buffer[i]

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
					print("Error: P table overflow")
					sys.exit()
				P = PTYPE()
				P.address = module_address + address
				P_table[P_tablex] = P
			elif firstchar == 'E':
				if E_tablex >= E_TABLE_SIZE:
					print("ERROR: E table overflow\n")
					sys.exit()
				E = ETYPE()
				E.address = module_address + address
				E_table[E_tablex] = E
			elif firstchar == 'R':
				if R_tablex >= R_TABLE_SIZE:
					print("ERROR: R table overflow\n")
					sys.exit()
				R = RTYPE()
				R.module_address = module_address
				R.address = module_address + address
				R_table[R_tablex] = R
				R_tablex += 1
				continue

			if firstchar == 'P':
				for j in range(0, P_tablex):
					if(firstchar == P_table[j].symptr):
						print("ERROR: Duplicate PUBLIC symbol " + firstchar)
						sys.exit()
				
				P_table[P_tablex].symptr = fptr
				P_tablex += 1
			elif firstchar == 'E':
				E_table[E_tablex].symptr = fptr
				E_tablex += 1

			i += 2
			fptr = file_buffer[i]
			continue
def doifile():
	global ifilename, out_stream, ofopen, file_buffer, ofilename
	
	if not(ifilename.endswith('.mob')):
		ifilename = ifilename + '.mob'
	
	file_buffer = []
	
	in_stream = open(ifilename, 'rb')
	with in_stream as file:
		byte = file.read(1)
		while byte != '':
			file_buffer.append(byte)
			byte = file.read(1)

	in_stream.close()
	
	if not(in_stream):
		print("ERROR: Cannot open input file" + ifilename)
		sys.exit()
	
	if not(ofopen):
		ofopen = 1
		ofilename = ifilename
		ofilename = ofilename.rsplit( ".", 1 )[ 0 ]	#rid of ./mob
		ofilename = ofilename + '.mac' #add .mac
	
		out_stream = open(ofilename, "wb")
			
		if not(out_stream):
			print("ERROR: Cannot open output file" + ofilename)
			sys.exit()
	
	processfile()

def main():
	global ifilename, out_stream, in_stream, E_tablexstart,R_tablexstart,P_tablexstart, text_buffer_size, module_address, R_table
	j = 0
	print("Author: Brandon Walsh")
	
	if len(sys.argv) < 3:
		print("ERROR: Incorrect number of command line args")
		sys.exit()
		
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
	
	'''
	if E_tablexstart != E_tablex:
		print("ERROR: Unresolved external symbol " + E_table[E_tablexstart].symptr)
		sys.exit()
	'''
	for R_tablexstart in range (R_tablexstart, R_tablex):
		text_buffer[R_table[R_tablexstart].address] = text_buffer[R_table[R_tablexstart].address] & 0xf000 | (text_buffer[R_table[R_tablexstart].address] + R_table[R_tablexstart].module_address) & 0x0fff

	for i in range (0, P_tablex):
		out_stream.write("P")
		out_stream.write(chr(int(str(P_table[i].address), 16)))
		out_stream.write(chr(00))
		out_stream.write(P_table[i].symptr)
		out_stream.write(chr(00))
		
	for i in range (0, R_tablex):
		out_stream.write("R")
		out_stream.write(chr(int(str(R_table[i].address), 16)))
		out_stream.write(chr(00))

	for i in range(0, E_tablex):
		out_stream.write("R")
		out_stream.write(chr(int(str(E_table[i].address), 16)))
		out_stream.write(chr(00))

	if gots:
		out_stream.write(saves)
		out_stream.write(startadd)

	out_stream.write("T")
	
	for k in range(0, text_buffer_size+8):
	#for k in range(0, module_address * 2): #this might work
		if text_buffer[k] != 255:
			out_stream.write(chr(text_buffer[k]))
			out_stream.write(chr(00))
		else:
			out_stream.write(chr(text_buffer[k]))
		
	out_stream.close()
	print "Output file: " + ofilename
	
main()