
from operator import itemgetter
from pprint import pprint

import pandas
import pandas as pd
from tkinter import filedialog as fd
excepted_scale_format = ['6144', '12288']
empty_par = {'name': '',
             'address': '',
             'editable': '',
             'description': '',
             'scale': '',
             # 'scaleB': '',
             'unit': '',
             'value': '',
             # 'scale_value': '',
             # 'scale_format': '',
             'type': '',
             # 'group': '',
             'period': ''}

file_name = fd.askopenfilename()
excel_data_df = pandas.read_excel(file_name)
nodes = excel_data_df.to_dict(orient='records')

# for param in params_list:
#     if str(param['editable']) != 'nan':

# root_node = ET.parse(file_name).getroot()
# nodes = root_node.findall('param')
final_list = []


for tag in nodes:
    tg = empty_par.copy()
    t = tag
    pprint(t)
    if 'Тип' in t.keys():
        v_type = t['Тип']
    elif 'type' in t.keys():
        v_type = t['type']
    else:
        print('No types ')
        break
    if v_type == 'UINT32':
        v_type = 'UNSIGNED32'
    elif v_type == 'UINT16':
        v_type = 'UNSIGNED16'
    elif v_type == 'INT16' or \
            v_type == 'UNION' or \
            v_type == 'STR':
        v_type = 'SIGNED16'
    elif v_type == 'INT32' or \
            v_type == 'DATE':
        v_type = 'SIGNED32'
    else:
        v_type = 'SIGNED32'

    if 'scale' in t.keys():
        scale = t['scale']
    elif 'Коэф-т' in t.keys():
        scale = t['Коэф-т']
    else:
        print('No scale ')
        break
    # scale = t['scale_value']
    # if int(scale) != 0:
    #     scale = 16777216 / int(scale)
    #
    # if t['scale_format'] in excepted_scale_format:
    #     v_type = 'SIGNED16'
    #     scale = 0
    #
    if 'name' in t.keys():
        tg['name'] = t['name']
    elif 'Название' in t.keys():
        tg['name'] = t['Название']
    else:
        print('No Название ')
        break

    if 'address' in t.keys():
        tg['address'] = t['address']
    elif 'Адрес' in t.keys():
        tg['address'] = t['Адрес']
    else:
        print('No address ')
        break

    if 'editable' in t.keys():
        tg['editable'] = t['editable']
    elif 'Запись' in t.keys():
        tg['editable'] = t['Запись']
    else:
        print('No Запись ')
        break

    if 'description' in t.keys():
        tg['description'] = t['description']
    elif 'Описание' in t.keys():
        tg['description'] = t['Описание']
    else:
        print('No Описание ')
        break

    if 'unit' in t.keys():
        tg['unit'] = t['unit']
    elif 'Ед. изм.' in t.keys():
        tg['unit'] = t['Ед. изм.']
    else:
        print('No Ед. изм. ')
        break

    if 'Размер' in t.keys():
        tg['size'] = t['Размер']
    elif 'size' in t.keys():
        tg['size'] = t['size']
    else:
        print('No size ')
        break

    if 'code' in t.keys():
        tg['code'] = t['code']
    elif 'Код' in t.keys():
        tg['code'] = t['Код']
    else:
        print('No code ')
        break

    # tg['address'] = hex(int(t['co_index'])) + hex(int(t['co_subindex']))[2:].zfill(2)
    # tg['editable'] = t['checked']
    # tg['description'] = t['EngText']
    tg['scale'] = scale
    # tg['unit'] = t['tdim']
    # tg['scale_value'] = t['scale_value']
    # tg['scale_format'] = t['scale_format']
    tg['type'] = v_type
    tg['period'] = 1
    if str(tg['address']) != 'nan':
        tg['address'] = hex(int(tg['address']))

            # tg['group'] = int(t['group_num'])  # возможно, здесь нужно делать проверку есть ли интежер, может,
    # здесь название группы

    final_list.append(tg.copy())
# final_list = sorted(final_list, key=itemgetter('group'))

old_par = empty_par
old_group = ''
f_list = []
for par in final_list:
    if par['code'].count('.') == 2:
        f_list.append(par)
    elif par['code'].count('.') == 1:
        par['name'] = 'group ' + str(par['name'])
        f_list.append(par)
    else:
        pass
df = pd.DataFrame(f_list, columns=tg.keys())

df.to_excel(file_name.split('.')[0] + '_parse.xlsx', index=False)
