# _*_ coding:utf-8 _*_

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests as res
import time
import obj
import re

ua = UserAgent()
user_agent = ua.chrome

headers = {
            'content-type': 'text/html; charset=utf-8', # attention code
            'content-encoding': 'gzip',
            'User-Agent': user_agent
        }

# 關鍵字解析器
def keyword_parser(url,headers):
    html = res.get(url=url,headers=headers)
    html = html.content
    soup = BeautifulSoup(html, 'html.parser')
    keywords_class = soup.find_all("div", attrs={"class": "td-post-source-tags"})

    keywords_ls = []
    for k in keywords_class:
        k = k.find_all(href=re.compile("\S{10}")) 
        for s in k:
            s = s.text
            keywords_ls += [s]
            
    return keywords_ls

# 新聞爬蟲
def crawler(headers,block):
    article_ls = []

    for page in range(1,20):    
        try:
            url = 'https://www.nownews.com/cat/'+ block +'/page/'+ str(page) +'/'
            html = res.get(url=url,headers=headers)
            html = html.content
            soup = BeautifulSoup(html, 'html.parser')
            artcle_url = soup.find_all("h3", attrs={"class": "entry-title td-module-title"})

            for i in artcle_url:
                i = i.find("a").get("href")
                article_ls += [i]

            time.sleep(3)

        except:
            break

    tag_ls = []
    for link in article_ls:
        keywords_ls = keyword_parser(link, headers)
        tag_ls += [keywords_ls]
        time.sleep(3)

    tags_ls = sum(tag_ls,[])
    
    return tags_ls


# 健康養生
def health_crawler_1(headers):
    href_ls = [] # 健康新聞文章連結

    for page in range(1,20):
        url = 'https://healthmedia.nownews.com/main.aspx?cid=1&page=' + str(page)
        html = res.get(url=url,headers=headers)
        html = html.content
        soup = BeautifulSoup(html, 'html.parser')
        url_class = soup.find_all("h3")

        for i in url_class:
            i = i.find(id=True)
            if i != None:
                h = "https://healthmedia.nownews.com/" + i.get("href")
                href_ls += [h]

    health_tag_ls = [] # 健康新聞 → 關鍵字

    for url in href_ls:
        html = res.get(url=url,headers=headers)
        html = html.content
        soup = BeautifulSoup(html, 'html.parser')
        tag_class = soup.find_all("div", attrs={"class": "tag"})
        time.sleep(3)

        for tag in tag_class:
            tag = tag.find_all(id=True)
            for t in tag:
                t = t.text
                health_tag_ls += [t]
    
    return health_tag_ls

# 醫美減重
def health_crawler_2(headers):
    href_ls = [] # 健康新聞文章連結

    for page in range(1,20):
        url = 'https://healthmedia.nownews.com/main.aspx?cid=2&page=' + str(page)
        html = res.get(url=url,headers=headers)
        html = html.content
        soup = BeautifulSoup(html, 'html.parser')
        url_class = soup.find_all("h3")

        for i in url_class:
            i = i.find(id=True)
            if i != None:
                h = "https://healthmedia.nownews.com/" + i.get("href")
                href_ls += [h]

    health_tag_ls = [] # 健康新聞 → 關鍵字

    for url in href_ls:
        html = res.get(url=url,headers=headers)
        html = html.content
        soup = BeautifulSoup(html, 'html.parser')
        tag_class = soup.find_all("div", attrs={"class": "tag"})
        time.sleep(3)

        for tag in tag_class:
            tag = tag.find_all(id=True)
            for t in tag:
                t = t.text
                health_tag_ls += [t]
    
    return health_tag_ls

# 兩性關係
def health_crawler_3(headers):
    href_ls = [] # 健康新聞文章連結

    for page in range(1,20):
        url = 'https://healthmedia.nownews.com/main.aspx?cid=2&page=' + str(page)
        html = res.get(url=url,headers=headers)
        html = html.content
        soup = BeautifulSoup(html, 'html.parser')
        url_class = soup.find_all("h3")

        for i in url_class:
            i = i.find(id=True)
            if i != None:
                h = "https://healthmedia.nownews.com/" + i.get("href")
                href_ls += [h]

    health_tag_ls = [] # 健康新聞 → 關鍵字

    for url in href_ls:
        html = res.get(url=url,headers=headers)
        html = html.content
        soup = BeautifulSoup(html, 'html.parser')
        tag_class = soup.find_all("div", attrs={"class": "tag"})
        time.sleep(3)

        for tag in tag_class:
            tag = tag.find_all(id=True)
            for t in tag:
                t = t.text
                health_tag_ls += [t]
    
    return health_tag_ls

############## 主程式 ###############
try:
    politics_keyword_ls = crawler(headers,'politics') # 政治
    entertainment_keyword_ls = crawler(headers,'entertainment') # 娛樂
    sport_keyword_ls = crawler(headers,'sport') # 運動
    house_keyword_ls = crawler(headers,'house') # 房地產
    finance_keyword_ls = crawler(headers,'finance') # 財經
    life_keyword_ls = crawler(headers,'life') # 生活
    society_keyword_ls = crawler(headers,'society') # 社會
    chinaindex_keyword_ls = crawler(headers,'chinaindex') # 大陸
    global_keyword_ls = crawler(headers,'global') # 國際

    # 健康養生 + 醫美減重 + 兩性關係
    h1,h2,h3 = health_crawler_1(headers),health_crawler_2(headers),health_crawler_3(headers)
    health_keyword_ls = h1 + h2 + h3  # 健康

    ######## 資料庫 #########
    # 插入政治 → 關鍵字
    table_name = "political_table"
    word_ls = list(set(politics_keyword_ls))
    obj.insert_data(word_ls,table_name)

    # 插入娛樂 → 關鍵字
    table_name = "entertainment_table"
    word_ls = list(set(entertainment_keyword_ls))
    obj.insert_data(word_ls,table_name)

    # 插入運動 → 關鍵字
    table_name = "sport_table"
    word_ls = list(set(sport_keyword_ls))
    obj.insert_data(word_ls,table_name)

    # 插入房地產 → 關鍵字
    table_name = "house_table"
    word_ls = list(set(house_keyword_ls))
    obj.insert_data(word_ls,table_name)

    # 插入財經 → 關鍵字
    table_name = "finance_table"
    word_ls = list(set(finance_keyword_ls))
    obj.insert_data(word_ls,table_name)

    # 插入生活 → 關鍵字
    table_name = "life_table"
    word_ls = list(set(life_keyword_ls))
    obj.insert_data(word_ls,table_name)

    # 插入社會 → 關鍵字
    table_name = "society_table"
    word_ls = list(set(society_keyword_ls))
    obj.insert_data(word_ls,table_name)

    # 插入大陸 → 關鍵字
    table_name = "chian_table"
    word_ls = list(set(chinaindex_keyword_ls))
    obj.insert_data(word_ls,table_name)

    # 插入國際 → 關鍵字
    table_name = "international_table"
    word_ls = list(set(global_keyword_ls))
    obj.insert_data(word_ls,table_name)

    # 插入健康 → 關鍵字
    table_name = "health_table"
    word_ls = list(set(health_keyword_ls))
    obj.insert_data(word_ls,table_name)

except:
    url = "https://maker.ifttt.com/trigger/toline/with/key/bTiIQ-E9vw_2N49lBCTa1i?value1=Nownews爬蟲失敗"
    res.get(url=url)

import pandas as pd
from bs4 import BeautifulSoup
import requests
import csv

headers = {
    'content-type': 'text/html; charset=Big5',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

url = "https://tw.stock.yahoo.com/s/list.php?c=%A4%F4%AAd&rr=0.07816700%201558667143"
html = requests.get(url,headers=headers,timeout=15)
html.apparent_encoding # 解碼中文字
html_text = html.text # 轉文字格式
df_1 = pd.read_html(html_text) # 回傳一個 list table
table = df_1[2] # 抓到表格

vendor_colum = table["股票代號"] # 索引股票代號的欄位
vendor_ls = vendor_colum.values.tolist() # DataFrame 轉 list

deal_colum = table["成交"] # 索引股票代號的欄位
deal_ls = deal_colum.values.tolist() # DataFrame 轉 list

quote_change_colum = table["漲跌"] # 索引股票代號的欄位
quote_change_ls = quote_change_colum.values.tolist() # DataFrame 轉 list

quantity_colum = table["張數"] # 索引股票代號的欄位
quantity_ls = quantity_colum.values.tolist() # DataFrame 轉 list