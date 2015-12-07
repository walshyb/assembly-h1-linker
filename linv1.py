#!/usr/bin/env python

'''
Python adapation of Anthony J. Dos Reis's H1 Assembler Module Linker.

Author: Brandon Walsh

'''

import sys, binascii

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
text_buff_index = 0
gots = False
saves = ''
ifilename = ''
ofilename = ''
text_buffer = [0] * (MACSIZE+1)	# holds instructions loaded from .mob file (everything after T entry)
file_buffer = []	# hex contents of loaded .mob file
in_stream = None
out_stream = None

def ierror():
	print("ERROR: Input file " + str(ifilename) + " is not linkable\n")
	sys.exit()

'''
Parse input files and place entries, addresses, and instructions into respective tables
'''
def processfile():
	global startadd, gots, module_address, P_table, E_table, R_table, P_tablex, E_tablex, R_tablex, text_buffer_size, text_buff_index
	i = 0
	address = 0
	endptr = file_buffer[len(file_buffer)-1]	# last 2 hex bits

	# get first item in file_buffer
	fptr = file_buffer[i]

	while True:

		# assign entry letter (P, E, R, T, or S) to firstchar
		firstchar = fptr

		i += 1
		fptr = file_buffer[i]

		if firstchar == 'T':
			textsize = len(file_buffer) - i
			text_buffer_size += textsize

			if textsize/2 > MACSIZE - module_address:
				print("ERROR: Linked program too big")
				sys.exit()

			iSave = i

			for k in range (0, textsize, 2):
				text_buffer[module_address] = file_buffer[i+1].encode('hex') + file_buffer[i].encode('hex')
				text_buffer[module_address] = int(text_buffer[module_address], 16)
				i = i + 2
				module_address += 1

			module_address -= 1
			module_address += textsize/2
			break

		if firstchar != 'S' and firstchar != 's' and firstchar != 'P' and firstchar != 'E' and firstchar != 'R':
			ierror()
		else:

			#get 2 bytes (1 word) of hex data (current file_buffer location and next)
			address = file_buffer[i+1].encode('hex') + fptr.encode('hex')

			#convert hex data to int
			address = int(address, 16)

			i += 2
			fptr = file_buffer[i]	# assign symbol for current entry to fptr

			# if position "i" is greater than length of file_buffer
			if i > len(file_buffer)-1:
				ierror()

			# if S entry
			if firstchar == 'S' or firstchar == 's':	# 'S' is relative address (specified by a label), 's' is absolute address

				# if starting address already specified
				if gots:
					print("ERROR: More than one starting address")
					sys.exit()

				gots = True
				saves = firstchar

				if firstchar == 'S':
					startadd = address
				else:
					startadd = address + module_address
				continue

			if firstchar == 'P':

				# if too many P Entries
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

				# for each index in P_table, check for duplicate symbols
				for j in range(0, P_tablex):
					if(fptr == P_table[j].symptr):
						print("ERROR: Duplicate PUBLIC symbol " + fptr)
						sys.exit()

				P_table[P_tablex].symptr = fptr
				P_tablex += 1 	#increment number of P entries
			elif firstchar == 'E':
				E_table[E_tablex].symptr = fptr
				E_tablex += 1 	#increment number of E entries

			i += 2
			fptr = file_buffer[i]
			continue

'''
Assure proper input file extension and create output file
'''
def doifile():
	global ifilename, out_stream, ofopen, file_buffer, ofilename

	if not(ifilename.endswith('.mob')):
		ifilename = ifilename + '.mob'

	# reinitialize file_buffer to empty array
	file_buffer = []

	try:
		in_stream = open(ifilename, 'rb')
	except:
		print("ERROR: Cannot open input file " + ifilename)
		sys.exit()

	with in_stream as file:
		byte = file.read(1)
		while byte != '':
			file_buffer.append(byte)
			byte = file.read(1)

	in_stream.close()

	# if outfile not already created
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

'''
Populate output file with linked data
'''
def main():
	global ifilename, out_stream, in_stream, E_tablexstart,R_tablexstart,P_tablexstart, text_buffer_size, module_address, R_table
	j = 0
	print("Author: Brandon Walsh")

	# if 2 file names not specified
	if len(sys.argv) < 2:
		print("ERROR: Incorrect number of command line arguments")
		sys.exit()

	# for each command line argument
	for argx in range (1, len(sys.argv)):
		ifilename = sys.argv[argx]
		doifile()

	for E_tablexstart in range (E_tablexstart, E_tablex+1):
		j = 0

		while j < P_tablex and P_table[j].symptr != E_table[E_tablexstart].symptr:
		#while j < P_tablex and P_table[j].symptr == E_table[E_tablexstart].symptr:
			j += 1

		if j < P_tablex:
			text_buffer[E_table[E_tablexstart].address] = text_buffer[E_table[E_tablexstart].address] & 0xf000 | (text_buffer[E_table[E_tablexstart].address] + P_table[j].address ) & 0x0fff
		else:
			break
	
	#E_tablexstart += 1 #add one because loop above doesn't run inclusively
	
	# if there is an extra E entry
	if E_tablexstart != E_tablex:
		print("ERROR: Unresolved external symbol " + E_table[E_tablexstart].symptr)
		sys.exit()
	
	for R_tablexstart in range (R_tablexstart, R_tablex):
		text_buffer[R_table[R_tablexstart].address] = text_buffer[R_table[R_tablexstart].address] & 0xf000 | (text_buffer[R_table[R_tablexstart].address] + R_table[R_tablexstart].module_address) & 0x0fff


	# =============== Write to Out File ============
	# write P Entries
	for i in range (0, P_tablex):
		out_stream.write('P')

		# convert int address to 4-bit hex string
		temp = format(P_table[i].address, '04x') 

		# flip first two bits with last two
		temp = temp[2:] + temp[2:-2] + temp[:2]

		out_stream.write(binascii.a2b_hex(temp))	# convert hex string to binary encoded hex and write address of P entry
		out_stream.write(P_table[i].symptr)			# write symbol (assume symbol is one letter)
		out_stream.write(chr(00))					# write padding to make symbol 4 digits

	# write R Entries
	for i in range (0, R_tablex):
		out_stream.write("R")

		# convert int address to 4-bit hex string
		temp = format(R_table[i].address, '04x')

		# flip first two bits with last two
		temp = temp[2:] + temp[2:-2] + temp[:2]

		# convert hex string to binary encoded hex and write address of R entry
		out_stream.write(binascii.a2b_hex(temp))

	# write E Entries (as R entries)
	for i in range(0, E_tablex):
		out_stream.write("R")

		# convert int address to 4-bit hex string
		temp = format(P_table[i].address, '04x')

		# flip first two bits with last two
		temp = temp[2:] + temp[2:-2] + temp[:2]

		# convert hex string to binary encoded hex and write address of E entry (as R Entry)
		out_stream.write(binascii.a2b_hex(temp))

	# if starting address specified (S Entry), then write starting address
	if gots:
		out_stream.write(saves)
		out_stream.write(startadd)

	out_stream.write("T")

	# write instructions (located in text_buffer)
	for k in range(0, 2 * module_address):

		# convert int address to 4-bit hex string
		temp = format(text_buffer[k], '04x')

		# flip first two bits with last two
		temp = temp[2:] + temp[2:-2] + temp[:2]

		# convert hex string to binary encoded hex and write instruction
		out_stream.write(binascii.a2b_hex(temp))

	out_stream.close()
	print "Output file: " + ofilename

main()