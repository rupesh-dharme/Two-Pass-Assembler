import json

ST = json.load(open('./Tables/ST.json', 'r'))
LT = json.load(open('./Tables/LT.json', 'r'))
MOT = json.load(open('./Tables/MOT.json', 'r'))

def convert_to_list(line):
    line = line[:-1]
    l = line.strip().replace('     ', '-').replace('   ', '-').split('-')
    if l[0][:2] == 'lc':
        l.pop(0)
    return l

def convert_to_machine(l):
    s = []
    if l[0][1:3] == 'IS' or l[0][1:3] == 'DL':
        s.append(l[0][5:7])
    if len(l)>1 and l[1][0]=='(' and l[1][2]==')':
        s.append('0'+l[1][1])
    if len(l)>2:
        if l[-1][1] == 'L':
            for k, v in LT.items():
                if str(v[0]) == l[-1][4]:
                    s.append(str(v[1]))
        elif l[-1][1] == 'S':
            for k, v in ST.items():
                if str(v[0]) == l[-1][4]:
                    s.append(str(v[1]))
    if len(s) == 1:
        s += ['00', '000']
    return ' '.join(s)

if __name__ == '__main__':
    with open('IR.txt', 'r') as file:
        lines = file.readlines()

    code = []

    for line in lines:
        l = convert_to_list(line)
        if l[0][1:3] == 'AD' or l[0][1:3] == 'DS': continue
        s = convert_to_machine(l)
        code.append(s)
    
    with open('target.txt', 'w') as file:
        file.write('\n'.join(code)+'\n')