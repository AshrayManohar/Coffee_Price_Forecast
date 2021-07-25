# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 09:04:02 2021

@author: THOTAAM1
"""
### This script is used to read PDF files to get the coffee prices
import re
import PyPDF2
from datetime import datetime
import os
import pandas as pd

final=pd.DataFrame()
year_lst=['2021'] #['2015','2016','2017','2018','2019','2020','2021']

for year in year_lst:
    os.chdir(r"C:\Learning\Coffee_Commodity_Price\Data\\" + year)
    wd_path=os.getcwd()
    months_lst=os.listdir(wd_path)
    
    for mon in months_lst:
        #year='2020'
        #mon='Dec'
        temp=pd.DataFrame()
        mon_wd_path=os.chdir(wd_path +"\\"+ mon)      
        files=os.listdir(mon_wd_path)
        
#wd_path=os.getcwd()
#os.listdir(wd_path)

        dates=[]
        price=[]
            
        for file in files:
            print(file)
            
            pdfFileObj = open(wd_path+"\\"+mon+"\\"+file, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            pageObj = pdfReader.getPage(0)
            text=pageObj.extractText()
            text=text.replace('\n', "")
            
            a, b = text.find('Cents/lb Rs/Kg'), text.find('Futures Price Trend')
            price.append(float(text[a:b].split(")")[-2].split("(")[0][:-3]))
            
            c, d = text.find('Coffee Market Report'), text.find('Futures Prices')
            
            year=text[c+21:d].strip().replace(",","").strip().split(" ")[-1] #text[c+21:d].strip().split(",")[-1].strip()
            month=text[c+21:d].strip().replace(",","").strip().split(" ")[-3] #text[c+21:d].strip().split(",")[-2].strip().split(" ")[0]
            date=text[c+21:d].strip().replace(",","").strip().split(" ")[-2] #text[c+21:d].strip().split(",")[-2].strip().split(" ")[1]
            date=re.sub("[^0-9]", "", date).zfill(2)
            dates.append(datetime.strptime(year+"-"+month+"-"+date,'%Y-%B-%d'))

        temp['Dates']=dates
        temp['Price']=price
        temp['Year']=year
        temp['Month']=month
    
        final=pd.concat([final,temp])
        
        
        
final.to_csv(r"C:\Learning\Coffee_Commodity_Price\Data\Output\",index=False)       


data=pd.read_csv(r"C:\Learning\Coffee_Commodity_Price\Final_Data.csv")



data.columns

data.groupby(by='Month')['Price'].mean()/data['Price'].mean()

 