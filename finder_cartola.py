import openpyxl as xl
import pandas as pd

path = '/Users/fneut/Desktop/PP/cartola.xls'
df = pd.read_excel(path,usecols = "B:G")
first_row_with_all_NaN = df[df.notnull().all(axis=1) == True].index.tolist()[0] #
df = pd.read_excel(path,header=first_row_with_all_NaN+1,usecols = "B:G") #excel - 1
first_row_with_all_NaN = df[df.isnull().all(axis=1) == True].index.tolist()[0] #
df = df.loc[0:first_row_with_all_NaN-1]


file_name = "/Users/fneut/Documents/Desktop/PP/SalidaData2.csv"
df.to_csv(file_name, sep=',', index = False)

