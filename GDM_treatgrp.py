# Searches for key words that identify GDM treatment groups in PeriBank metadata
# Found instances of search terms will be summerized in a new last column of the output spreadsheet
# Updated 19 Nov 2022, Maxim Seferovic, seferovi@bcm.edu

#!/usr/bin/env python3

searchterms={
    'insulin':[
        'Insulin',
        'Novolog',
        'Humalog',
        'Insulina',
        'Novolin', 
        'Humulin',
        'Lispro',
        'Glulisine',
        'Aspart',
        'Apidra',
        'Detemir',
        'Levemir',
        'Lantus',
        'Basaglar',
        'Glargine',
        'Toujeo',
        'Degludec',
	],
    'metformin':[
        'Metformin',
        'Metfomin',
        'glucophage',
        'glucophage XR',
        'glucophageXR',
        'fortamet',
        'glumetza',
        'riomet'
	],
}

def strp (var):
    var = var.strip().lower()
    var = '|'.join(var.split('\t'))
    return var

name = input("Enter file to append string (Enter for 'PBDBwMetformin.txt'): ")
if len(name) == 0 : name = "PBDBwMetformin.txt"

outlist = {}
with open(name) as f: 
    firstline = f"{strp(f.readline())}|insulin terms|metformin terms|neither[0],insulin[1],metformin[2],both[3]{chr(10)}"
    for line in f:  
        line = strp(line)
        ID = line.split('|')

        try:
            for v in searchterms.values():    
                foundterms=[]
                for term in v:
                    if line.find(term.lower()) != -1: foundterms.append(term.lower())
                line += '|' + ','.join(foundterms)
            outlist[int(ID[1])] = line
        except: print ('Parsing error: ', line)

for k,v in sorted(outlist.items()):
    line = v.split('|')
    if line[-2] == '' and line[-1] == '': i = '0'
    elif line[-2] != '' and line[-1] == '': i = '1'
    elif line[-2] == '' and line[-1] != '': i = '2'
    elif line[-2] != '' and line[-1] != '': i = '3'
    outlist[k] = f"{v}|{i}"

savename = input("Save as (Blank - exit without saving, d - default: ")
if len(savename) == 0: quit()
if savename == "d": savename = "Searched_cohort.txt"

with open(savename,'w') as f: 
    f.write(f"sep=|{chr(10)}{firstline}")
    f.write('\n'.join(outlist.values()))
