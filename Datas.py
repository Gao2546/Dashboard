import pandas as pd
import os
import re
import numpy as np

class data:
    def __init__(self):
        self.data = {}
    def add_data(self,data,fname):
        s = re.split('_',fname)
        year = s[1]
        month = s[0][:-1]
        month_p = s[0][-1]
        month_cp = s[-1]
        if year not in self.data:
            self.data[year] = {}
            self.data[year][month] = {}
            self.data[year][month][month_p] = {}
            self.data[year][month][month_p][month_cp] = data
        elif month not in self.data[year]:
            self.data[year][month] = {}
            self.data[year][month][month_p] = {}
            self.data[year][month][month_p][month_cp] = data
        elif month_p not in self.data[year][month]:
            self.data[year][month][month_p] = {}
            self.data[year][month][month_p][month_cp] = data
        else :
            self.data[year][month][month_p][month_cp] = data
    def add_all_in_folder(self,dir):
        self.dir = dir
        l_data = os.listdir(self.dir)
        for i in l_data:
            self.add_data(i,i[:-4])
        return l_data
    def read_data(self,data):
        if (re.split('_',data)[-1] == 'contract.csv') or (re.split('_',data)[-1] == 'clean.csv'):
            return pd.read_csv(self.dir+'/'+data,encoding='utf-8')
        else:
            return pd.read_csv(self.dir+'/'+data,usecols=[0,2,3,4],encoding='utf-8')

def cleandata(df):
    subdep_name = df['subdep_name'].unique()
    subdep_name = subdep_name.tolist()
    subdep_name.sort()
    s = set()
    for i in subdep_name:
        for ii in i:
            s.add(ii)
    dic = {}
    for n,i in enumerate(s):
        dic[i] = n
    a = []
    for k in subdep_name:
        j = np.zeros(shape=(160,140))
        for n,i in enumerate(k):
            j[n,dic[i]] = 1
        a.append(j)
    #subdep_name = subdep_name[11:]
    #a = a[11:]
    mapping = {}
    start = 0
    curr = 1
    mapp = 0
    mapping[subdep_name[start]] = mapp
    while(True):
        try:
            #u = int((min([len(subdep_name[start]),len(subdep_name[curr])]))//1.2)
            ls = [len(re.split('[\d," "]',(subdep_name[start]).strip())[0]),len(re.split('[\d," "]',(subdep_name[curr]).strip())[0])]
            u = int((min(ls))//1)
            jj = a[start][:u] == a[curr][:u]
            st = 0
            stp = 1
            k = 0.8
            t = 0.3
            if not(re.findall("โรงเรียน",subdep_name[start]) and re.findall("โรงเรียน",subdep_name[curr]) or 
                   re.findall("โรงพยาบาล",subdep_name[start]) and re.findall("โรงพยาบาล",subdep_name[curr]) or
                   re.findall("เทศบาลตำบล",subdep_name[start]) and re.findall("เทศบาลตำบล",subdep_name[curr]) or 
                   re.findall("เขตรักษาพันธุ์สัตว์ป่า",subdep_name[start]) and re.findall("เขตรักษาพันธุ์สัตว์ป่า",subdep_name[curr]) or
                   re.findall("อุทยานแห่งชาติ",subdep_name[start]) and re.findall("อุทยานแห่งชาติ",subdep_name[curr]) or 
                   re.findall("องค์การบริหารส่วนตำบล",subdep_name[start]) and re.findall("องค์การบริหารส่วนตำบล",subdep_name[curr]) or
                   re.findall("สำนักงานเขต",subdep_name[start]) and re.findall("สำนักงานเขต",subdep_name[curr]) or
                   re.findall("ศูนย์พัฒนาเด็กเล็ก",subdep_name[start]) and re.findall("ศูนย์พัฒนาเด็กเล็ก",subdep_name[curr]) or 
                   re.findall("ที่ทำการปกครองอำเภอ",subdep_name[start]) and re.findall("ที่ทำการปกครองอำเภอ",subdep_name[curr]) or
                   re.findall("การไฟฟ้าส่วนภูมิภาค",subdep_name[start]) and re.findall("การไฟฟ้าส่วนภูมิภาค",subdep_name[curr]) or 
                   re.findall("การประปาส่วนภูมิภาค",subdep_name[start]) and re.findall("การประปาส่วนภูมิภาค",subdep_name[curr]) or 
                   re.findall("กศน.",subdep_name[start]) and re.findall("กศน.",subdep_name[curr]) or 
                   re.findall("วิทยาลัยเทคนิค.",subdep_name[start]) and re.findall("วิทยาลัยเทคนิค.",subdep_name[curr])
                   ): 
                #print(subdep_name[curr])
                if u/int((max(ls))//1) < 0.65 or len(subdep_name[curr]) < 20 :
                    #print(subdep_name[curr])
                    k = 1
                    t = 0.05
                for i in range(int(k*u)):
                    if jj[i].sum() != 104:
                        st += 1
                try:
                    if (st/round(k*u)) > t:
                        stp = 0
                except:
                    pass
            else:
                #print(subdep_name[start])
                stp = 1

            if stp:
                #print(subdep_name[curr])
                mapping[subdep_name[curr]] = mapp
                start = curr
                curr += 1

            else:
                mapp += 1
                start = curr
                curr += 1
                #u = int((min([len(re.split('[\d," "]',subdep_name[start])[0]),len(re.split('[\d," "]',subdep_name[curr])[0])]))//1.2)
                mapping[subdep_name[start]] = mapp
        except:
            #print(KeyError.with_traceback())
            break
    return mapping

    
        