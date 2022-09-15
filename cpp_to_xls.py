from operator import itemgetter
from pprint import pprint

import pandas as pd
from tkinter import filedialog as fd
empty_par = {'name': '',
             'address': '',
             'editable': '',
             'description': '',
             'scale': '',
             'scaleB': '',
             'unit': '',
             'value': '',
             'type': '',
             'group': '',
             'period': '',
             'size': '',
             'degree': ''}

file_name = fd.askopenfilename()
with open(file_name, "r") as file:
    nodes = file.readlines()

final_list = []


for tag in nodes:
    tg = empty_par.copy()
    if 'OD_' in tag:
        t = tag.split(',')
        tg['name'] = t[4].strip()[1:-1]
        tg['group'] = t[3].strip()[1:-1]
        tg['address'] = t[0].strip()[2:] + t[1].strip()[2:-1]
        v_type = t[6].strip()[3:]
        if v_type == 'UINT32':
            v_type = 'UNSIGNED32'
        elif v_type == 'FUNC' or \
                v_type == 'STRING' or \
                v_type == 'ENUM':
            v_type = 'UNSIGNED16'
        elif v_type == 'FLOAT32':
            v_type = 'FLOAT'
        else:
            v_type = 'SIGNED32'
        tg['type'] = v_type
        if t[5] != '""':
            tg['unit'] = t[5].strip()[1:-1]
        if t[8] == 'true':
            tg['editable'] = 1
#         if 'RW' in t[2]:
#             tg['editable'] = 1
#         tg['name'] = t[4].strip()[30:-1]
#     if tg['name']:
        final_list.append(tg.copy())

final_list = sorted(final_list, key=itemgetter('group'))
pprint(len(final_list))

old_par = empty_par
old_group = ''
f_list = []
for par in final_list:
    if par['group'] != old_group:
        old_group = par['group']
        old_par['name'] = 'group ' + str(par['group'])
        f_list.append(old_par.copy())
    f_list.append(par)

df = pd.DataFrame(f_list, columns=tg.keys())

df.to_excel(file_name.split('.')[0] + '_parse.xlsx', index=False)
pprint(len(f_list))
