import pandas as pd
import numpy as np
import sys
import codecs
import datetime

def to_IgorTable(filename):
    with codecs.open(filename, "r", "Shift-JIS", "ignore") as file:
        column_list = ['sample', 'x', 'y']
        raw_data = pd.read_table(file, delimiter='\t', names = column_list)
        raw_data = raw_data.drop([0])

    data = raw_data.fillna(method='ffill')
    
    #sample列を", "で分割し、cell列とdye列を作成 -> data_1
    data_1 = pd.concat([data, data['sample'].str.split(', ', expand=True)], axis=1).drop('sample', axis = 1)
    data_1 = data_1.rename(columns={0: 'cell'})
    data_1 = data_1.rename(columns={1: 'dye'})

    #x列にTemperature(-C)が格納されている行を削除
    #dye列がSYBRであるもののみ取得 -> data_1
    data_1 = data_1[data_1["x"] != "Temperature (ｰC)"]
    data_1 = data_1[data_1["dye"] == "SYBR"]

    # data_2にセルごとのデータを区切って格納
    salts = ["A", "B", "C", "D", "E", "F", "G", "H"]
    pHs = (list(range(1,13)))
    data_2 = pd.DataFrame()
    temp = pd.DataFrame()

    for salt in salts:
        for pH in pHs:
            temp = pd.DataFrame()
            well = salt + str(pH)
            temp = data_1[data_1['cell'] == well].drop(['cell', 'dye'], axis=1)
            temp = temp.dropna(how='all')
            temp = temp.reset_index()
            data_2 = pd.concat([data_2, temp["x"], temp["y"]], axis=1)
            data_2 = data_2.rename(columns={'x': well + "_x", 'y': well + '_y'})

    result_file = str(datetime.date.today()) + "_SSS2_table.csv"
    data_2.to_csv(result_file)

if __name__ =="__main__":
    to_IgorTable(sys.argv[1])
