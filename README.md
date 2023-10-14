# -
使用爬蟲及自動化流程搜尋地震資料並標記在可操作地圖之中

## 爬蟲操作部分

from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup

import time

import pandas as pd

import  re
#constant

cwbUrl = 'https://scweb.cwb.gov.tw'

# Create Chrome Page

options = Options()

options.add_argument("--disable-notifications")  

chrome = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options )

year=2021
month=12
quake ={"編號":[],"日期":[],"時間":[],"震央位置":[],"緯度":[],"經度":[],"相對位置":[],"震度":[],"規模":[],"深度":[]}
for year in range(2012,2022):
    
    for month in range(1,13):
        
        print(str(year) + '年' + str(month) + '月')
        
        #打開網址(中央氣象局 地震測報中心)
        chrome.get(cwbUrl+'/zh-tw/earthquake/data/')
        
        ## setup search Month
        #月份查詢絕對路徑
        xpath='/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/h2/input[1]' #xpath of quakelist table
        #擷取元素
        searchMonth = chrome.find_element("xpath",xpath)
        #運行javascript
        chrome.execute_script('arguments[0].removeAttribute(\"readonly\")', searchMonth)
        #刪除搜尋框文字
        chrome.find_element("xpath",xpath).clear()
        #傳入搜尋字串
        searchMonth.send_keys(str(year)+'年'+str(month)+'月')
        #搜尋(enter)
        searchMonth.send_keys(Keys.RETURN)
 
        ## setup list opion to 'All
        #頁數絕對路徑
        xpath='/html/body/div[1]/div[2]/div/div[2]/div[1]/div[4]/div/div[1]/div/div[2]/div/label/select' #option xpath
        #擷取元素
        tableLength=chrome.find_element("xpath",xpath)
        #從下拉列表中選擇選項(All)
        Select(tableLength).select_by_index(5) 
    
        ##get html contain
        #推遲調用線程的運行
        time.sleep(3)
        #解析網頁
        soup = BeautifulSoup(chrome.page_source, 'html.parser')
        
        quakeTable = soup.find_all('table')[1].find_all('tr')
    
        for row in quakeTable[1:]:
    
            col = row.find_all('td')
            #編號
            number = col[0].text  
            #震度
            vibration = col[1].text  
            #時間
            quaketime = col[2].text[6:]
            #規模
            magnitude = col[3].text  
            #深度
            depth = col[4].text  
            #相對位置
            position = col[5].text
            #日期
            date = col[6].text[:10]  
            #網址
            quakeList = cwbUrl+col[6].find('a')['href']  
            
            ##地震的詳細資料
            chrome.get(quakeList)
            
            time.sleep(2)  
            
            soup = BeautifulSoup(chrome.page_source, 'html.parser')
            
            infoList = soup.find_all('li')
            #震央位置
            for i in range(len(infoList)):
    
                if '震央位置' in infoList[i].text:
                   
                    #震央
                    latlot = infoList[i].text.split('\n')[2]  
                    #緯度
                    #pattern1 = r'北緯 \d{2}.\d(\d)?'
                    
                    pattern = latlot.split('北緯')[1]
                    
                    lat = pattern.split('東經')[0]
                    
                    lat = lat.split('°')[0]
                    
                    #northlat=re.findall(pattern1,infoList[i].text)
                    
                    #pattern11 = r'\d{2}.\d(\d)?'
                    
                    #lat=re.findall(pattern11,str(northlat))
                    
                    #lat="".join(lat)
                    #經度
                    pattern2 = r'東經 \d\d\d.\d(\d)?'
                     
                    lot = pattern.split('東經')[1]
                    
                    lot = lot.split('°')[0]

                    
                    #westlot=re.findall(pattern2,infoList[i].text)
                    
                    #pattern22 = r'\d\d\d.\d(\d)?'
                    
                    #lot=re.findall(pattern22,str(westlot))
                    
                    #lot="".join(lot)
                    # exit loop i
                    break     
            
            #傳入dataframe      
            quake['編號'].append(number)
            quake['日期'].append(date)
            quake['時間'].append(quaketime)
            quake['震央位置'].append(latlot)
            quake['緯度'].append(lat)
            quake['經度'].append(lot)
            quake['相對位置'].append(position)
            quake['震度'].append(vibration)
            quake['規模'].append(magnitude)
            quake['深度'].append(depth)
          
            

df_quake = pd.DataFrame(quake)
df_quake.to_csv('地震(2012-21).csv',encoding='utf-8-sig',index=False)

##
