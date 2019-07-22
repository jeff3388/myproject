# _*_ coding:utf-8 _*_

from bs4 import BeautifulSoup
import requests as res
import datetime
import sqlite3
import time
import csv
import obj
import re

s = res # requests

headers = {
            'content-type': 'text/html; charset=utf-8', # attention code
            'content-encoding': 'gzip',
            'server': 'nginx',
            'status': '200',
            'vary': 'Accept-Encoding',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'accept': 'text/html,application/xhtml+xml,application/xml;'
            'q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Referer': 'https://www.ettoday.net/events/passback/scupio/ad_300x600_2_FL-HB-2.htm',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            '(KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
        }

################################ 主程式 ###################################

### 收集政治、社會、生活、國際、大陸、財經等新聞文章連結 ####
try:
    # 政治
    political_link = 'https://www.ettoday.net/news/focus/%E6%94%BF%E6%B2%BB/'
    political_tags_ls = obj.collage_keyword(political_link,headers,s)
    # 社會
    society_link = 'https://www.ettoday.net/news/focus/%E7%A4%BE%E6%9C%83/'
    society_tags_ls = obj.collage_keyword(society_link,headers,s)
    # 生活
    life_link = 'https://www.ettoday.net/news/focus/%E7%94%9F%E6%B4%BB/'
    life_tags_ls = obj.collage_keyword(life_link,headers,s)
    # 國際
    international_link = 'https://www.ettoday.net/news/focus/%E5%9C%8B%E9%9A%9B/'
    international_tags_ls = obj.collage_keyword(international_link,headers,s)
    # 大陸
    chian_link = 'https://www.ettoday.net/news/focus/%E5%A4%A7%E9%99%B8/'
    chian_tags_ls = obj.collage_keyword(chian_link,headers,s)
    # 財經
    finance_link = 'https://www.ettoday.net/news/focus/%E8%B2%A1%E7%B6%93/'
    finance_tags_ls = obj.collage_keyword(finance_link,headers,s)
    
except:
    url = "https://maker.ifttt.com/trigger/toline/with/key/bTiIQ-E9vw_2N49lBCTa1i?value1=ETtoday爬蟲失敗-政社生國大財"
    res.get(url=url)

########################### 雲論新聞主題文章連結 ##############################
try:
    url = 'https://forum.ettoday.net/newslist/'
    html = s.get(url,headers=headers,timeout=15).content
    w = obj.cloud_parser_page(html)
    w = int(w) + 1

    cloud_article_ls = [] # 所有雲論新聞連結
    for page in range(1,w):
        url = 'https://forum.ettoday.net/newslist/' + str(page)
        html = s.get(url,headers=headers,timeout=15).content
        cloud_url_ls = obj.cloud_article_link(html)
        time.sleep(3)

        for c in cloud_url_ls:
            cloud_article_ls += [c]

    cloud_tag_ls = [] # 雲論新聞 → 關鍵字
    for cloud_url in cloud_article_ls:
        html = s.get(cloud_url,headers=headers,timeout=15).text
        soup = BeautifulSoup(html, 'html.parser')
        part_tag_class = soup.find_all("div", attrs={"class": "part_tag"})
        time.sleep(3)

        for tag in part_tag_class:
            tag_ls = tag.text.split("\n")

            for y in tag_ls: 
                if y not in ['','關鍵字:','雲論']:
                    cloud_tag_ls += [y]
    
except:
    url = "https://maker.ifttt.com/trigger/toline/with/key/bTiIQ-E9vw_2N49lBCTa1i?value1=ETtoday爬蟲失敗-雲論"
    res.get(url=url)
                
############################ 娛樂新聞主題文章連結 ###############################
try:
    entertainment_url_ls = [] # 娛樂連結
    for page in range(1,6):
        url ='https://star.ettoday.net/news-focus/%E5%8D%B3%E6%99%82/9/'+str(page)
        html = s.get(url,headers=headers,timeout=15).content
        entertainment_article_ls = obj.entertainment_article_link(html)
        time.sleep(5)

        for e in entertainment_article_ls:
            entertainment_url_ls += [e]

    entertainment_tag_ls = [] # 娛樂新聞 → 關鍵字

    for entertainment_url in entertainment_url_ls:
        html = s.get(entertainment_url,headers=headers,timeout=15).content
        soup = BeautifulSoup(html, 'html.parser')
        tag_class = soup.find_all("div", attrs={"class": "menu_txt_2"})
        time.sleep(3)

        for t in tag_class:
            t = t.text
            t = re.sub(r'[\n：關鍵字 ]', '', t).split(",")
            for q in t:
                entertainment_tag_ls += [q]
    
except:
    url = "https://maker.ifttt.com/trigger/toline/with/key/bTiIQ-E9vw_2N49lBCTa1i?value1=ETtoday爬蟲失敗-娛樂"
    res.get(url=url)
            
############################# 健康主題新聞連結 ##########################
try:
    health_ls =['https://health.ettoday.net/category/%E5%81%A5%E5%BA%B7%E7%84%A6%E9%BB%9E/', # 健康焦點
                'https://health.ettoday.net/category/%E9%86%AB%E8%97%A5%E6%96%B0%E8%81%9E/', # 醫藥新聞
                'https://health.ettoday.net/category/%E9%A3%B2%E9%A3%9F/', # 飲食新聞
                'https://health.ettoday.net/category/%E7%BE%8E%E9%AB%94/', # 美體新聞
                'https://health.ettoday.net/category/%E5%85%A9%E6%80%A7/', # 兩性新聞
                'https://health.ettoday.net/category/%E8%A6%AA%E5%AD%90/', # 親子新聞
                'https://health.ettoday.net/category/%E4%B8%AD%E9%86%AB/', # 中醫新聞
                'https://health.ettoday.net/category/%E7%99%BE%E7%A7%91/', # 百科新聞
                'https://health.ettoday.net/category/%E5%AF%B5%E7%89%A9/', # 寵物新聞
               ]

    health_article_ls = [] # 健康連結

    for health_url in health_ls:
        health_url_ls = obj.health_web(health_url,headers)
        time.sleep(2)

        for h in health_url_ls:
            health_article_ls += [h]

    health_tag_ls = [] # 健康新聞 → 關鍵字
    for health_link in health_article_ls:
        html = s.get(health_link,headers=headers,timeout=15).content
        soup = BeautifulSoup(html, 'html.parser')
        tag_class = soup.find_all("div", attrs={"class": "tag"})
        time.sleep(3)

        for tag in tag_class:
            tag = tag.text
            key_str = re.sub(r'[關鍵字： 雲論]', '', tag)
            key = key_str.split("\n")

            for k in key:
                if k not in ['']:
                    health_tag_ls += [k]
    
except:
    url = "https://maker.ifttt.com/trigger/toline/with/key/bTiIQ-E9vw_2N49lBCTa1i?value1=ETtoday爬蟲失敗-健康"
    res.get(url=url)

########################## 旅遊新聞文章連結 ############################
try:
    url = 'https://travel.ettoday.net/focus/%E6%96%B0%E8%81%9E%E7%84%A6%E9%BB%9E/?&page=1'
    html = s.get(url,headers=headers,timeout=15).content
    w = obj.cloud_parser_page(html) # 獲得網頁頁數
    w = int(w) + 1 

    travel_url_ls = [] # 旅遊連結
    for page in range(1,w):
        url ='https://travel.ettoday.net/focus/%E6%96%B0%E8%81%9E%E7%84%A6%E9%BB%9E/?&page='+ str(page)
        html = s.get(url,headers=headers,timeout=15).content
        article_url_ls = obj.travel_article_link(html)
        time.sleep(5)

        for url in article_url_ls:
            travel_url_ls += [url]

    travel_tag_ls = [] # 旅遊新聞 → 關鍵字

    for travel_url in travel_url_ls:
        html = s.get(travel_url,headers=headers,timeout=15).content
        soup = BeautifulSoup(html, 'html.parser')
        tag_class = soup.find_all("div", attrs={"class": "tag"})
        time.sleep(3)

        for tag in tag_class:
            tag = tag.text
            key_str = re.sub(r'[關鍵字： 雲論]', '', tag)
            key_ls = key_str.split("\n")

            for k in key_ls:
                if k not in ['']:
                    travel_tag_ls += [k]
except:
    url = "https://maker.ifttt.com/trigger/toline/with/key/bTiIQ-E9vw_2N49lBCTa1i?value1=ETtoday爬蟲失敗-旅遊"
    res.get(url=url)


######################### 房地產新聞文章連結 #########################
try:
    url = 'https://house.ettoday.net/index/1'
    html = s.get(url,headers=headers).content
    w = obj.parser_page(html)
    w = int(w) + 1

    house_article_url = [] # 房地產連結
    for page in range(1,w):
        target_url = 'https://house.ettoday.net/index/' + str(page) 
        html = s.get(target_url,headers=headers,timeout=15).content
        house_url_ls = obj.house_article_link(html)
        time.sleep(3)
        for house in house_url_ls:
            house_article_url += [house]

    house_tag_ls = [] # 房地產新聞 → 關鍵字

    for house_url in house_article_url:
        html = s.get(house_url,headers=headers,timeout=15).content
        soup = BeautifulSoup(html, 'html.parser')
        tag_class = soup.find_all("p", attrs={"class": "tag"})
        time.sleep(3)

        for tag in tag_class:
            tag = tag.text
            key_str = re.sub(r'[關鍵字： 雲論]', '', tag)
            key_ls = key_str.split("\n")

            for k in key_ls:
                if k not in ['']:
                    if '﹑' in k:
                        k = k.split("﹑")
                        for v in k:
                            house_tag_ls += [v]
                    elif '、' in v:
                        k = k.split("、")
                        for v in k:
                            house_tag_ls += [v]
                    else:
                        house_tag_ls += [k]
except:
    url = "https://maker.ifttt.com/trigger/toline/with/key/bTiIQ-E9vw_2N49lBCTa1i?value1=ETtoday爬蟲失敗-房地產"
    res.get(url=url)
                    
        
#################### 體育新聞關鍵字 ######################

try:
    url_dit ={  # 連結順序 → SLB新聞、中職新聞、NBA新聞、足球新聞、競技新聞
    'https://sports.ettoday.net/news-list/%E6%A3%92%E7%90%83/MLB/':'https://sports.ettoday.net/news-list/%E6%A3%92%E7%90%83/MLB/',
    'https://sports.ettoday.net/news-list/%E7%B1%83%E7%90%83/SBL/WSBL/':'https://sports.ettoday.net/news-list/%E7%B1%83%E7%90%83/SBL/WSBL/',
    'https://sports.ettoday.net/news-list/%E6%A3%92%E7%90%83/%E4%B8%AD%E8%81%B7/':'https://sports.ettoday.net/news-list/%E6%A3%92%E7%90%83/%E4%B8%AD%E8%81%B7/',
    'https://sports.ettoday.net/news-list/%E7%B1%83%E7%90%83/NBA/':'https://sports.ettoday.net/news-list/%E7%B1%83%E7%90%83/NBA/',
    'https://sports.ettoday.net/news-list/%E8%B6%B3%E7%90%83/%E5%9C%8B%E9%9A%9B%E5%8B%95%E6%85%8B/':'https://sports.ettoday.net/news-list/%E8%B6%B3%E7%90%83/%E5%9C%8B%E9%9A%9B%E5%8B%95%E6%85%8B/',
    'https://sports.ettoday.net/news-list/%E7%AB%B6%E6%8A%80/%E6%8A%80%E6%93%8A%E3%80%81%E7%90%83%E9%A1%9E/':'https://sports.ettoday.net/news-list/%E7%AB%B6%E6%8A%80/%E6%8A%80%E6%93%8A%E3%80%81%E7%90%83%E9%A1%9E/',

    }

    sport_tag_ls = [] # 運動關鍵字

    for url,target_url in url_dit.items():
        html = s.get(url,headers=headers,timeout=15).content
        web_pages = obj.parser_page(html) # 獲取網頁頁數
        w = int(web_pages) + 1
        tag_ls = obj.sport_tag(w,target_url,headers)
        time.sleep(5) # 每次請求停頓5秒

        for tag in tag_ls:
            if tag not in ['']:
                sport_tag_ls += [tag]
except:
    url = "https://maker.ifttt.com/trigger/toline/with/key/bTiIQ-E9vw_2N49lBCTa1i?value1=ETtoday爬蟲失敗-運動"
    res.get(url=url)


######## 資料庫 #########
# 插入政治 → 關鍵字
table_name = "political_table"
word_ls = list(set(political_tags_ls))
obj.insert_data(word_ls,table_name)

# 插入社會 → 關鍵字
table_name = "society_table"
word_ls = list(set(society_tags_ls))
obj.insert_data(word_ls,table_name)

# 插入生活 → 關鍵字
table_name = "life_table"
word_ls = list(set(life_tags_ls))
obj.insert_data(word_ls,table_name)

# 插入國際 → 關鍵字
table_name = "international_table"
word_ls = list(set(international_tags_ls))
obj.insert_data(word_ls,table_name)

# 插入大陸 → 關鍵字
table_name = "chian_table"
word_ls = list(set(chian_tags_ls))
obj.insert_data(word_ls,table_name)

# 插入財經 → 關鍵字
table_name = "finance_table"
word_ls = list(set(finance_tags_ls))
obj.insert_data(word_ls,table_name)

# 插入雲論 → 關鍵字
table_name = "cloud_table"
word_ls = list(set(cloud_tag_ls))
obj.insert_data(word_ls,table_name)

# 插入娛樂 → 關鍵字
table_name = "entertainment_table"
word_ls = list(set(entertainment_tag_ls))
obj.insert_data(word_ls,table_name)

# 插入健康 → 關鍵字
table_name = "health_table"
word_ls = list(set(health_tag_ls))
obj.insert_data(word_ls,table_name)

# 插入旅遊 → 關鍵字
table_name = "tourism_table"
word_ls = list(set(travel_tag_ls))
obj.insert_data(word_ls,table_name)

# 插入房地產 → 關鍵字
table_name = "house_table"
word_ls = list(set(house_tag_ls))
obj.insert_data(word_ls,table_name)

# 插入運動 → 關鍵字
table_name = "sport_table"
word_ls = list(set(sport_tag_ls))
obj.insert_data(word_ls,table_name)
