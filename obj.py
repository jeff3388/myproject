# _*_ coding:utf-8 _*_
from bs4 import BeautifulSoup
import requests as res
import datetime
import sqlite3
import time
import csv
import re

db_name = '/home/cfd888/external_hdd/public_html/temp.check-article.cfd888.info/ETtoday_keyword.db'
# db_name = './ETtoday_keyword.db'
con = sqlite3.connect(db_name) 
c = con.cursor() # 建立連線物件

s = res # requests

### 獲取資料庫所有資料 ###
def get_all_data(table_name):
    key_ls = []
    with con:
        c.execute('SELECT * FROM '+ "'" + table_name + "'" + 'ORDER BY keyword')
        rows = c.fetchall()
        for row in rows:
            r = row[0]
            if r != '':
                key_ls += [r]
    return key_ls

# 統計資料庫關鍵字數量
def get_data(table_name):
    with con:
        c.execute('SELECT * FROM '+ "'" + table_name + "'" )
        rows = c.fetchall()
        number = str(len(rows))
        
        return number
    
# 統計數據寫入 CSV
def write_csv(datetime_str, political, society, life ,international ,chian ,finance ,cloud ,entertainment ,health ,travel,house,sport):
    with open('/home/cfd888/external_hdd/public_html/temp.check-article.cfd888.info/output.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # 寫入另外幾列資料
        writer.writerow([datetime_str, political, society, life, international ,chian ,finance ,cloud ,entertainment ,health ,travel,house,sport])

# 確認表格是否存在，不存在則建立
def if_table_not_exist(table_name):
    c.execute('CREATE TABLE IF NOT EXISTS'+ "'" + table_name + "'" +'( keyword TEXT PRIMARY KEY )')

# 單筆資料
def insert_data(word_ls,table_name):
    if_table_not_exist(table_name)
    with con:
        for word in word_ls:
            try:
                c.execute('INSERT INTO'+ "'" + table_name + "'" +'(keyword) VALUES (?)',[word])
            except Exception as e:
                print(e)
                
        con.commit() # 提交資料
                
                    

# 政治、社會、生活、國際、大陸、財經用解析器
def article_link(html):
    soup = BeautifulSoup(html, 'html.parser') 
    piece_clearfix = soup.find_all("div", attrs={"class": "piece clearfix"})

    article_url_ls = []
    
    for p in piece_clearfix:
        p = p.find('a').get('href')
        m = re.findall('/news.*htm',p)
        if m != []:
            m = "https://www.ettoday.net" + "".join(m)
            article_url_ls += [m]
            
    return article_url_ls

# 健康新聞用解析器
def health_article_link(html):
    soup = BeautifulSoup(html, 'html.parser')
    piece_clearfix = soup.find_all("div", attrs={"class": "piece clearfix"})

    article_url_ls = []
    
    for p in piece_clearfix:
        p = p.find('a').get('href')
        m = re.findall('https:\/\/health.ettoday.net\/news\/\d{7}',p)
        if m != []:
            m = "".join(m)
            article_url_ls += [m]
            
    return article_url_ls


# 娛樂新聞用解析器
def entertainment_article_link(html):
    soup = BeautifulSoup(html, 'html.parser')
    title_a = soup.find_all("h3", attrs={"class": "title_a"})
    menu_page = soup.find_all("div", attrs={"class": "menu_page"})
    
    article_url_ls = []
    
    for t in title_a:
        t = t.find("a").get("href")
        m = re.findall("\/new.*",t)
        if m != []:
            m = 'https://star.ettoday.net' + "".join(m)
            article_url_ls += [m]
            
    return article_url_ls

# 旅遊新聞解析器
def travel_article_link(html):
    soup = BeautifulSoup(html, 'html.parser')
    title_a = soup.find_all("a", attrs={"class": "pic"})

    article_url_ls = []
    
    for t in title_a:
        t = t.get("href")
        m = re.findall("\/article.*",t)
        if m != []:
            m = 'https://travel.ettoday.net' + "".join(m)
            article_url_ls += [m]
    
    return article_url_ls

# 雲論新聞解析器
def cloud_article_link(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find_all("h2", attrs={"class": "title"})

    article_url_ls =[]
    
    for t in title:
        t = t.find('a').get('href')
        m = re.findall("https:\/\/forum.ettoday.net\/news.*",t)
        if m != []:
            m = "".join(m)
            article_url_ls += [m]

    return article_url_ls

# 單一運動新聞 tag 解析器
def sport_parser_tag(html):
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all("p", attrs={"class": "tag"})

    tag_ls = []
    
    for tag in tags:
        tag = tag.text
        tag = re.sub(r'[關鍵字： \r]', '', tag)
        tag_ls += [tag]

    t_ls = "".join(tag_ls).split("\n")
    
    return t_ls

# 解析網頁有多少頁數
def parser_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    web_pages = soup.find_all("p", attrs={"class": "info"})[0].text
    web_pages = re.sub(r'[第頁共]', '', web_pages)
    web_pages = web_pages.split("|")[1]
    
    return web_pages


# 解析雲論網頁有多少頁數
def cloud_parser_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    web_pages = soup.find_all("p", attrs={"class": "info"})

    page_ls = []
    
    for w in web_pages:
        w = w.text
        page_ls += [w]

    page_str = "".join(page_ls).split("|")[1].split("(")[0]
    page = re.sub(r'[共頁 ]', '', page_str)
    
    return page

# 所有運動新聞文章關鍵字解析器
def sport_tag(w,target_url,headers):
    keyword_ls = []
    
    for page in range(1,w):    
        url = target_url + str(page) # MLB新聞
        html = s.get(url,headers=headers).content
        tag_ls = sport_parser_tag(html)
        
        for k in tag_ls:
            keyword_ls += [k]
        
    return keyword_ls

# 健康新聞主題文章連結解析器
def health_web(health_url,headers):
    health_url_ls = []
    
    for page in range(1,6):
        try:
            url = health_url + str(page)
            html = s.get(url,headers=headers).content
            health_ls = health_article_link(html)
            for health in health_ls:
                health_url_ls +=[health]
        except:
            pass
        
    return health_url_ls

# 房地產新聞主題文章連結解析器
def house_article_link(html):
    soup = BeautifulSoup(html, 'html.parser')
    box_class = soup.find_all("div", attrs={"class": "pic"})

    house_url_ls = []
    
    for box in box_class:
        box = box.find("a").get("href")
        b1 = re.findall('\/\/house.ettoday.net\/news\/\d{7}',box)
        if b1 != []:
            b1 = 'https:' + "".join(b1)
            house_url_ls += [b1]
            
    return house_url_ls

def collage_keyword(url,headers,s):
    article_url_ls = [] # 文章連結

    html = s.get(url,headers=headers).content
    url_ls = article_link(html)
    time.sleep(5)

    for link in url_ls:
        article_url_ls += [link]

    article_tags = [] # 文章關鍵字

    for art_url in article_url_ls:
        html = s.get(art_url,headers=headers,timeout=15).content
        soup = BeautifulSoup(html, 'html.parser')
        tag_class = soup.find_all("p", attrs={"class": "tag"})
        time.sleep(5)

        for tag in tag_class:
            tag = tag.text.replace("關鍵字：","").split(",")
            for t in tag:
                t = re.sub(r'[\r\n ]', '', t)
                if t != '':
                    if '﹑' in t:
                        t = t.split("﹑")
                        for v in t:
                            article_tags += [v]
                    elif '、' in t:
                        t = t.split("、")
                        for v in t:
                            article_tags += [v]
                    else:
                        article_tags += [t]
                        
    return article_tags