from operator import itemgetter

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
type_dict = {2: 'SIGNED8',
             3: 'SIGNED16',
             4: 'SIGNED32',
             5: 'UNSIGNED8',
             6: 'UNSIGNED16',
             7: 'UNSIGNED32',
             8: 'FLOAT'}

tg = empty_par.copy()

file_name = fd.askopenfilename()
final_list = []
with open(file_name, "r") as file:
    for line in file:
        if '[' in line:
            print(tg)
            final_list.append(tg.copy())
            tg = empty_par.copy()
            tg['address'] = '0x' + line.strip()[1:5]
            if 'sub' in line:
                tg['address'] += line.strip()[8:-1].zfill(2)

        if 'ParameterName' in line:
            tg['name'] = line.strip()[14:]
            if len(tg['address']) < len('0x000000'):
                tg['address'] = ''
                tg['name'] = 'group ' + tg['name']
        if 'ObjectType' in line:
            tg['size'] = line.strip()[11:]
        if 'DataType' in line:
            v_type = line.strip()[9:]
            v_type = int(v_type, 16)
            if v_type in list(type_dict.keys()):
                tg['type'] = type_dict[v_type]
        if 'AccessType=rw' in line:
            tg['editable'] = 1
        if 'DefaultValue' in line:
            tg['value'] = line.strip()[13:]

df = pd.DataFrame(final_list, columns=tg.keys())

df.to_excel(file_name.split('.')[0] + '_parse.xlsx', index=False)
