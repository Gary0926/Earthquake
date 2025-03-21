from collections import defaultdict
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
import pandas as pd

cwbUrl = 'https://scweb.cwa.gov.tw' # 中央氣象局的地震資料網頁
quake = defaultdict(list)           # 存放地震資料

# 開啟瀏覽器
options = Options()
options.add_argument("--headless")               # 隱藏瀏覽器
options.add_argument("--disable-notifications")  # 關閉通知
chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

for year in range(2024,2025):   
    for month in range(1,13):        
        print(f"{year} 年 {month} 月")
        
        # 打開網址(中央氣象局 地震測報中心)
        chrome.get(cwbUrl+'/zh-tw/earthquake/data/') 

        # 輸入日期
        xpath = "//h2/input[@type='text']" 
        searchMonth = chrome.find_element(By.XPATH, xpath)
        chrome.execute_script('arguments[0].removeAttribute(\"readonly\")', searchMonth) # 移除 readonly 屬性，可直接輸入日期
        chrome.find_element(By.XPATH, xpath).clear()
        searchMonth.send_keys(str(year)+'年'+str(month)+'月')
        searchMonth.send_keys(Keys.RETURN) 

        # 選擇地震資料
        dropdown = WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.XPATH, "//label/select")))
        Select(dropdown).select_by_index(5) # 選擇第 5 個屬性: All
        time.sleep(3)

        #解析網頁
        soup = BeautifulSoup(chrome.page_source, 'html.parser')        
        quakeTable = soup.find_all('table')[1].find_all('tr')

        for row in quakeTable[1:]:
            col = row.find_all('td')
            number = col[0].text                         # 編號        
            vibration = col[1].text                      # 震度    
            quaketime = col[2].text[6:]                  # 時間         
            magnitude = col[3].text                      # 規模        
            depth = col[4].text                          # 深度
            position = col[5].text                       # 相對位置
            date = col[6].text[:10]                      # 日期
            quakeList = cwbUrl+col[6].find('a')['href']  # 網址

            # 地震的詳細資料
            chrome.get(quakeList)  
            time.sleep(2)  
            soup = BeautifulSoup(chrome.page_source, 'html.parser')
            infoList = soup.find_all('li')

            # 震央位置
            for info in infoList:

                if '震央位置' in info.text:           
                    # 震央
                    latlot = info.text.split('\n')[2]  
                    # 緯度
                    pattern = latlot.split('北緯')[1]  
                    lat = pattern.split('東經')[0].split('°')[0] 
                    # 經度
                    pattern2 = r'東經 \d\d\d.\d(\d)?'  
                    lot = pattern.split('東經')[1].split('°')[0]
                
                    break   

            # 傳入dataframe      
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
df_quake.to_csv('地震(2024).csv',encoding='utf-8-sig',index=False)