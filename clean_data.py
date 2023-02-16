import Datas
import pandas as pd
import numpy as np
import re
def clean_map():
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
        for i in range(n-1):
            dfsub = df1[size*i:size*(i+1)]
            if i == n-2:
                dfsub = df1[size*i:]
            dfsub['subdep_id'] = dfsub['subdep_name'].replace(mapping)
            if not i:
                datass = dfsub
            if i:
                datass =  pd.concat([datass,dfsub],axis=0)
        datass.to_csv(f'use_data/{ii[:-4]}_clean.csv',encoding='utf-8',index=False)
        #datass.to_excel(f'clean_data1/{ii[:-4]}_clean.xlsx',encoding='utf-8',index = False)

def selec_class_T(n):
    mapdata_unique = {}
    data = Datas.data()
    l_data = data.add_all_in_folder('use_data')
    for ii in [l_data[3]]:
        df = data.read_data(ii)
        for i in df['subdep_id'].unique():
            if (df["subdep_id"] == i).sum() < n:
                df = df[df["subdep_id"] != i]
            else:
                drop_data = df.where(df['subdep_id'] == i).dropna()
                selec = min([len(drop_data.iloc[0]['subdep_name']),len(drop_data.iloc[-1]['subdep_name']),len(drop_data.iloc[-49]['subdep_name'])])
                mapdata_unique[i] = ''.join(np.array(re.split('',drop_data.iloc[0]['subdep_name'][:selec]))[(np.array(re.split('',drop_data.iloc[0]['subdep_name'][:selec])) == np.array(re.split('',drop_data.iloc[-1]['subdep_name'][:selec]))).tolist() and (np.array(re.split('',drop_data.iloc[0]['subdep_name'][:selec])) == np.array(re.split('',drop_data.iloc[-49]['subdep_name'][:selec]))).tolist()])
                if i == 9656:
                    mapdata_unique[i] = "โรงเรียน"
                if i == 211:
                    mapdata_unique[i] = "กลุ่มงานเภสัชกรรม โรงพยาบาล"
        print(mapdata_unique)
        df['subdep_class'] = df['subdep_id'].replace(mapdata_unique)
        df.to_csv(f'use_data/{ii}',encoding='utf-8',index=False)

