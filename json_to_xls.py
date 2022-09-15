import pandas
from tkinter import filedialog as fd

file_name = fd.askopenfilename()

pandas.read_json(file_name).to_excel(file_name.split('.')[0] + '_parse.xlsx')
