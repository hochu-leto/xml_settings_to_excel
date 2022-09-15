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
             'scale_value': '',
             'scale_format': '',
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
    if ' // ' in tag:
        tg['name'] = 'group ' + tag.strip()[3:]
    elif 'static_cast' in tag:
        t = tag.split(',')
        tg['address'] = t[0].strip()[8:] + hex(int(t[1].strip()))[2:].zfill(2)
        tg['type'] = t[2].strip()[3:-16]
        if 'RW' in t[2]:
            tg['editable'] = 1
        tg['name'] = t[4].strip()[30:-1]
    if tg['name']:
        final_list.append(tg.copy())
df = pd.DataFrame(final_list, columns=tg.keys())

df.to_excel(file_name.split('.')[0] + '_parse.xlsx', index=False)
