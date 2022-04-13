import pandas as pd

read_file = pd.read_excel (r'D:\Sercop\Mantis\Mantis 8842\correlacion_importar.xlsx')
read_file.to_csv (r'D:\Sercop\Mantis\Mantis 8842\correlacion_importar1.csv', sep='~', index = None, header=True)