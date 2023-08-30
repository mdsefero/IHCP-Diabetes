# Searches for key words that idenfigy metformin in PeriBank metadata
# Found instances of search terms will be summerized in a new last column of the output spreadsheet
# Updated 15 Nov 2022, Maxim Seferovic, seferovi@bcm.edu

#!/usr/bin/env python3

searchterms=[
	'Metformin',
	'Metfomin',
    'glucophage',
    'glucophage XR',
    'glucophageXR',
    'fortamet',
    'glumetza',
    'riomet'
	]

def strp (var):
    var = (var.strip() + '|').lower()
    var = '|'.join(var.split('\t'))
    return var

name = input("Enter file to append string (Enter for 'PBDBwMetformin.txt'): ")
if len(name) == 0 : name = "PBDBwMetformin.txt"

multiples = dict()
outlist = dict()
with open(name) as f: 
    firstline = strp(f.readline()) + 'found search terms|metformin\n'
    for line in f:  
        line = strp(line)
        ID = line.split('|')

        try:
            for term in searchterms:
                if line.find(term.lower()) != -1: line += term.lower() + '|yes'
            if line[-4:] != '|yes': line += '|no'
            if ID[0] in multiples.keys(): multiples[ID[0]] += 1
            else: multiples[ID[0]] = 1
            key =  ID[0] + '-' + str(multiples[ID[0]])
            outlist[key] = [int(ID[0]), line + '\n']
        except: print ('Likely truncated missing subject ID : ', line)

savename = input("Save as (Blank - exit without saving, d - default: ")
if len(savename) == 0: quit()
if savename == "d": savename = "Metformin_cohort_searched.txt"

f = open(savename,'w')
f.write('sep=|\n')
f.write(firstline)
for key, value in sorted(outlist.items(), key=lambda item: item[1]): f.write (value[1])
f.close()