import pandas as pd
from tkinter import filedialog as fd
empty_par = {'Время': '',
             'Момент двигателя': '',
             'Скорость двигателя': '',
             'Ток статора двигателя': '',
             'Скорость переднего левого колеса': '',
             'Скорость переднего правого колеса': '',
             'Скорость заднего левого колеса': '',
             'Скорость заднего правого колеса': ''}

file_name = fd.askopenfilename()
with open(file_name, "r") as file:
    nodes = file.readlines()

final_list = []
tg = empty_par.copy()

for tag in nodes:
    stroka = tag.split()

    if '18FF53A1' in tag:
        final_list.append(tg.copy())
        tg = empty_par.copy()
        tg['Время'] = stroka[16].strip().split(':')[2]
        tg['Момент двигателя'] = round(int((stroka[8].strip() + stroka[7].strip()), 16) / 100 - 100, 2)
        # print(f'{tg["Момент двигателя"]=}')
        tg['Скорость двигателя'] = round(int((stroka[10].strip() + stroka[9].strip()), 16) / 4 - 8000, 2)
        # print(f'{tg["Скорость двигателя"]=}')
        tg['Ток статора двигателя'] = round(int((stroka[12].strip() + stroka[11].strip()), 16) / 10 - 2000, 2)
        # print(f'{tg["Ток статора двигателя"]=}')
    if '10FF60A1' in tag:
        tg['Скорость переднего левого колеса'] = round(int((stroka[7].strip() + stroka[6].strip()), 16) / 500 - 50, 2)
        # print(f'{tg["Скорость переднего левого колеса"]=}')
        tg['Скорость переднего правого колеса'] = round(int((stroka[9].strip() + stroka[8].strip()), 16) / 500 - 50, 2)
        # print(f'{tg["Скорость переднего левого колеса"]=}')
        tg['Скорость заднего левого колеса'] = round(int((stroka[11].strip() + stroka[10].strip()), 16) / 500 - 50, 2)
        # print(f'{tg["Скорость переднего левого колеса"]=}')
        tg['Скорость заднего правого колеса'] = round(int((stroka[13].strip() + stroka[12].strip()), 16) / 500 - 50, 2)
        # print(f'{tg["Скорость переднего левого колеса"]=}')

df = pd.DataFrame(final_list, columns=tg.keys())

df.to_excel(file_name + '_parse.xlsx', index=False)
