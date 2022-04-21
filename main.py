import xml.etree.ElementTree as ET
from operator import itemgetter

import pandas as pd
from tkinter import filedialog as fd
excepted_scale_format = ['6144', '12288']
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
             'period': ''}

file_name = fd.askopenfilename()
root_node = ET.parse(file_name).getroot()
nodes = root_node.findall('param')
final_list = []


for tag in nodes:
    tg = empty_par.copy()
    t = tag.attrib

    v_type = t['tdim']
    if v_type == 'U32':
        v_type = 'UNSIGNED32'
    elif v_type == 'U16':
        v_type = 'UNSIGNED16'
    elif v_type == 'U8' or \
            v_type == 'перечисление' or \
            v_type == 'десятерич.' or \
            v_type == 'двоич.':
        v_type = 'UNSIGNED8'
    elif v_type == 'I16vparam':
        v_type = 'SIGNED16'
    elif v_type == 'I32':
        v_type = 'SIGNED32'
    else:
        v_type = 'SIGNED32'

    scale = t['scale_value']
    if int(scale) != 0:
        scale = 16777216 / int(scale)

    if t['scale_format'] in excepted_scale_format:
        v_type = 'SIGNED16'
        scale = 0

    tg['name'] = t['FullText']
    tg['address'] = hex(int(t['co_index'])) + hex(int(t['co_subindex']))[2:].zfill(2)
    tg['editable'] = t['checked']
    tg['description'] = t['EngText']
    tg['scale'] = scale
    tg['unit'] = t['tdim']
    tg['scale_value'] = t['scale_value']
    tg['scale_format'] = t['scale_format']
    tg['type'] = v_type
    tg['group'] = int(t['group_num'])  # возможно, здесь нужно делать проверку есть ли интежер, может,
    # здесь название группы

    final_list.append(tg.copy())
final_list = sorted(final_list, key=itemgetter('group'))

old_par = empty_par
old_group = ''
f_list = []
for par in final_list:
    if par['group'] != old_group:
        old_group = par['group']
        old_par['name'] = 'group ' + str(par['name'])
        f_list.append(old_par.copy())
    else:
        if par['unit'] != 'корень':
            f_list.append(par)
df = pd.DataFrame(f_list, columns=tg.keys())

df.to_excel(file_name.split('.')[0] + '_parse.xlsx', index=False)
