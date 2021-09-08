import pandas as pd
import json

MOT = {
    'MOVER':  ['IS', '01', 3],
    'MOVEM':  ['IS', '02', 3],
    'MULT':   ['IS', '03', 3],
    'ADD':    ['IS', '04', 1],
    'COMP':   ['IS', '05', 1],
    'BC':     ['IS', '06', 1],
    'READ':   ['IS', '07', 2],
    'DIV':    ['IS', '08', 2],
    'PRINT':  ['IS', '09', 2],
    'STOP':   ['IS', '00', 2],
    'SUB':    ['IS', '10', 1] }
ADs = {
    'START':  ['AD', '01', 0],
    'END':    ['AD', '02', 0],
    'ORIGIN': ['AD', '03', 0],
    'EQU':    ['AD', '04', 0],
    'LTORG':  ['AD', '05', 0] }
CCs = {
    'LT': 1,
    'LE': 2,
    'EQ': 3,
    'GT': 4,
    'GE': 5,
    'ANY': 6 }
ST = {}
LT = {}

def parts(line):
    label = line[:8]
    if label == '        ': label = ''
    neumonic = line[8:16].rstrip()
    op = line[16:].split(',')
    if op[0] == '': op = [] 
    else: op[-1] = op[-1][:-1].strip()
    return label.strip(), neumonic, op

def form(op):
    global literal_counter
    global symbol_counter
    if len(op) == 0 or op[0] == '':
        return ''
    elif len(op) == 2:
        if op[0][1:] == 'REG':
            op[0] = f'({ord(op[0][0])-64})'
        elif op[0] in CCs.keys():
            op[0]= f'({CCs[op[0]]})'
        if op[1][0] == '=':
            if op[1] not in LT.keys():
                literal_counter += 1
                LT[op[1]] = [literal_counter]
            op[1] = f'(L, {LT[op[1]][0]})'
        else:
            if op[1] not in ST.keys():
                symbol_counter += 1
                ST[op[1]] = [symbol_counter]
            op[1] = f'(S, {ST[op[1]][0]})'
        return op[0]+'   '+op[1]
    else:
        if op[0].isnumeric(): return f'(C, {op[0]})'
        elif op[0][0] == "'" and op[0][-1] == "'": return f'(C, {op[0][1:-1]})'
        elif '+' in op[0] or '-' in op[0]:
            i = op[0].find('+')
            if i == -1: i = op[0].find('-')
            suffix = op[0][i:]
            op[0] = op[0][:i]
            if op[0] not in ST.keys():
                symbol_counter += 1
                ST[op[0]] = [symbol_counter]
            return f'(S, {ST[op[0]][0]}){suffix}'
        else:
            if op[0] not in ST.keys():
                symbol_counter += 1
                ST[op[0]] = [symbol_counter]
            return f'(S, {ST[op[0]][0]})'

def inADs():
    global lc
    global symbol_counter
    global literal_counter
    if neumonic == 'START':
        IR.append('            (AD, 01)   (C, %s)\n' % str(op[0]).strip())
        lc = int(op[0])
        print()
    elif neumonic == 'LTORG':
        for i in LT.keys():
            lc+=1
            LT[i].append(lc)
    else:
        if label:
            if label in ST.keys(): ST[label].append(lc)
            else:
                symbol_counter += 1
                ST[label] = [symbol_counter, lc]
        ops = form(op)
        IR.append('lc: %d     (%s, %s)   %s\n' %
                  (lc, ADs[neumonic][0], ADs[neumonic][1], ops))
        print()
        lc += ADs[neumonic][2]

def inDLs():
    global lc
    global symbol_counter
    global literal_counter
    if label:
        if label in ST.keys(): ST[label].append(lc)
        else:
            symbol_counter += 1
            ST[label] = [symbol_counter, lc]
    ops = form(op)
    IR.append('lc: %d     (%s, %s)   %s\n' %
              (lc, 'DL', '01' if neumonic == 'DS' else '02', ops))
    print()
    lc += 1

def inISs():
    global lc
    global symbol_counter
    global literal_counter
    if label:
        if label in ST.keys(): ST[label].append(lc)
        else:
            symbol_counter += 1
            ST[label] = [symbol_counter, lc]
    ops = form(op)
    IR.append('lc: %d     (%s, %s)   %s\n' %
              (lc, MOT[neumonic][0], MOT[neumonic][1], ops))
    print()
    lc += MOT[neumonic][2]

if __name__ == "__main__":
    with open('Inputs/asm1.txt', 'r') as source:
        lines = source.readlines()
        
    IR = []
    symbol_counter = 0
    literal_counter = 0

    for line in lines:
        label, neumonic, op = parts(line)
        print(line.rstrip(), end=' ')
        if neumonic in ADs.keys():
            inADs()
        elif neumonic in ['DS', 'DC']:
            inDLs()
        else:
            inISs()

    print()
    print(pd.Series(ST))
    with open('Outputs/IR.txt', 'w') as ir:
        ir.writelines(IR)
    
    json.dump(ST, open('./Tables/ST.json', 'w'))
    json.dump(LT, open('./Tables/LT.json', 'w'))
    json.dump(MOT, open('./Tables/MOT.json', 'w'))