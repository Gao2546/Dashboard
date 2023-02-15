import Datas
import pandas as pd
n = 50
data = Datas.data()
l_datas = data.add_all_in_folder('data_sum')
for ii in l_datas:
    print(ii.split('_')[-1])
    if ii.split('_')[-1] != 'contract.csv':
        continue
    df1 = data.read_data(ii)
    df1 = df1.iloc[:,[2,3,10,14]]
    df1 = df1.dropna()
    size = df1.size
    size = size//n #fast & save ram
    mapping = Datas.cleandata(df1)
    s = 1
    for i in range(n-1):
        dfsub = df1[size*i:size*(i+1)]
        if i == n-2:
            dfsub = df1[size*i:]
        dfsub['subdep_id'] = dfsub['subdep_name'].replace(mapping)
        if not i:
            datass = dfsub
        if i:
            datass =  pd.concat([datass,dfsub],axis=0)
        s = 0
    datass.to_csv(f'use_data/{ii[:-4]}_clean.csv',encoding='utf-8')
    #datass.to_excel(f'clean_data1/{ii[:-4]}_clean.xlsx',encoding='utf-8')
