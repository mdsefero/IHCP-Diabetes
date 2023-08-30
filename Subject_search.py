# Searches for key words that idenfigy IHCP patients in PeriBank metadata
# Found instances will be summerized in a new last column of the output spreadsheet

#!/usr/bin/env python3

searchterms=[
	'IHCP',
	'ICP',
	'ICHP',
	'cholestasis',
	'cholelithiasis',
	'Ursodiol',
	]

def strp (var):
	var = var.strip("\n")
	#var = '\t'.join(var.split('|'))
	var = var + '|'
	return var

name = input("Enter file to append string (Enter for 'PBDBfinal'): ")
if len(name) == 0 : name = "PBDBfinal.txt"

multiples = dict()
outlist = dict()
handle1 = open(name)
for line in handle1:
	line = strp(line)
	ID = line.split('|')
	if ID[0].find('Pregnancy ID') != -1: firstline = line[1:] + 'Found Search Terms\n'
	else:
		try:
			for term in searchterms:
				if line.lower().find(term.lower()) != -1: line =  line + ' ' + term	
			if ID[0] in multiples.keys(): multiples[ID[0]] += 1
			else: multiples[ID[0]] = 1
			key =  ID[0] + '-' + str(multiples[ID[0]])
			outlist[key] = [int(ID[0]), line + '\n']
		except: print ('Likely truncated missing subject ID : ', line)
handle1.close()

savename = input("Save as (Blank - exit without saving, d - default: ")
if len(savename) == 0: quit()
if savename == "d": savename = "IHCP_Cohort.txt"

f = open(savename,'w')
f.write('sep=|\n')
f.write(firstline)
for key, value in sorted(outlist.items(), key=lambda item: item[1]): f.write (value[1])
f.close()