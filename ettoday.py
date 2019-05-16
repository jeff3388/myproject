from bs4 import BeautifulSoup
import requests as res
import datetime
import sqlite3
import time
import csv
import re

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
################################ 主程式 ###################################


### 收集政治、社會、生活、國際、大陸、財經等新聞文章連結 ####

s = res # requests

# 政治
political_link = 'https://www.ettoday.net/news/focus/%E6%94%BF%E6%B2%BB/'
political_tags_ls = collage_keyword(political_link,headers,s)
# 社會
society_link = 'https://www.ettoday.net/news/focus/%E7%A4%BE%E6%9C%83/'
society_tags_ls = collage_keyword(society_link,headers,s)
# 生活
life_link = 'https://www.ettoday.net/news/focus/%E7%94%9F%E6%B4%BB/'
life_tags_ls = collage_keyword(life_link,headers,s)
# 國際
international_link = 'https://www.ettoday.net/news/focus/%E5%9C%8B%E9%9A%9B/'
international_tags_ls = collage_keyword(international_link,headers,s)
# 大陸
chian_link = 'https://www.ettoday.net/news/focus/%E5%A4%A7%E9%99%B8/'
chian_tags_ls = collage_keyword(chian_link,headers,s)
# 財經
finance_link = 'https://www.ettoday.net/news/focus/%E8%B2%A1%E7%B6%93/'
finance_tags_ls = collage_keyword(finance_link,headers,s)

########################### 雲論新聞主題文章連結 ##############################
url = 'https://forum.ettoday.net/newslist/'
html = s.get(url,headers=headers,timeout=15).content
w = cloud_parser_page(html)
w = int(w) + 1

cloud_article_ls = [] # 所有雲論新聞連結
for page in range(1,w):
    url = 'https://forum.ettoday.net/newslist/' + str(page)
    html = s.get(url,headers=headers,timeout=15).content
    cloud_url_ls = cloud_article_link(html)
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
                

############################ 娛樂新聞主題文章連結 ###############################
entertainment_url_ls = [] # 娛樂連結
for page in range(1,6):
    url ='https://star.ettoday.net/news-focus/%E5%8D%B3%E6%99%82/9/'+str(page)
    html = s.get(url,headers=headers,timeout=15).content
    entertainment_article_ls = entertainment_article_link(html)
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
            
############################# 健康主題新聞連結 ##########################
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
    health_url_ls = health_web(health_url,headers)
    time.sleep(2)
    
    for h in health_url_ls:
        health_article_ls += [h]

health_tag_ls = [] # 健康新聞 → 關鍵字
for health_link in health_article_ls:
    try:
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
    except Exception as e:
        print(e)

########################## 旅遊新聞文章連結 ############################

url = 'https://travel.ettoday.net/focus/%E6%96%B0%E8%81%9E%E7%84%A6%E9%BB%9E/?&page=1'
html = s.get(url,headers=headers,timeout=15).content
w = cloud_parser_page(html) # 獲得網頁頁數
w = int(w) + 1 

travel_url_ls = [] # 旅遊連結
for page in range(1,w):
    url ='https://travel.ettoday.net/focus/%E6%96%B0%E8%81%9E%E7%84%A6%E9%BB%9E/?&page='+ str(page)
    html = s.get(url,headers=headers,timeout=15).content
    article_url_ls = travel_article_link(html)
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


######################### 房地產新聞文章連結 #########################
url = 'https://house.ettoday.net/index/1'
html = s.get(url,headers=headers).content
w = parser_page(html)
w = int(w) + 1

house_article_url = [] # 房地產連結
for page in range(1,w):
    target_url = 'https://house.ettoday.net/index/'+ str(page)
    html = s.get(target_url,headers=headers,timeout=15).content
    house_url_ls = house_article_link(html)
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
                    
        
#################### 體育新聞關鍵字 ######################

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
    web_pages = parser_page(html) # 獲取網頁頁數
    w = int(web_pages) + 1
    tag_ls = sport_tag(w,target_url,headers)
    time.sleep(5) # 每次請求停頓5秒
    
    for tag in tag_ls:
        if tag not in ['']:
            sport_tag_ls += [tag]


######## 資料庫 #########
db_name = '/home/cfd888/external_hdd/public_html/temp.check-article.cfd888.info/ETtoday_keyword.db'
con = sqlite3.connect(db_name) 
c = con.cursor() # 建立連線物件

# 插入政治 → 關鍵字
table_name = "political_table"
word_ls = list(set(political_tags_ls))
insert_data(word_ls,table_name)

# 插入社會 → 關鍵字
table_name = "society_table"
word_ls = list(set(society_tags_ls))
insert_data(word_ls,table_name)

# 插入生活 → 關鍵字
table_name = "life_table"
word_ls = list(set(life_tags_ls))
insert_data(word_ls,table_name)

# 插入國際 → 關鍵字
table_name = "international_table"
word_ls = list(set(international_tags_ls))
insert_data(word_ls,table_name)

# 插入大陸 → 關鍵字
table_name = "chian_table"
word_ls = list(set(chian_tags_ls))
insert_data(word_ls,table_name)

# 插入財經 → 關鍵字
table_name = "finance_table"
word_ls = list(set(finance_tags_ls))
insert_data(word_ls,table_name)

# 插入雲論 → 關鍵字
table_name = "cloud_table"
word_ls = list(set(cloud_tag_ls))
insert_data(word_ls,table_name)

# 插入娛樂 → 關鍵字
table_name = "entertainment_table"
word_ls = list(set(entertainment_tag_ls))
insert_data(word_ls,table_name)

# 插入健康 → 關鍵字
table_name = "health_table"
word_ls = list(set(health_tag_ls))
insert_data(word_ls,table_name)

# 插入旅遊 → 關鍵字
table_name = "tourism_table"
word_ls = list(set(travel_tag_ls))
insert_data(word_ls,table_name)

# 插入房地產 → 關鍵字
table_name = "house_table"
word_ls = list(set(house_tag_ls))
insert_data(word_ls,table_name)

# 插入運動 → 關鍵字
table_name = "sport_table"
word_ls = list(set(sport_tag_ls))
insert_data(word_ls,table_name)

# 獲取資料庫新聞關鍵字數量
political = get_data("political_table")         # 政治 → 關鍵字數量
society = get_data("society_table")             # 社會 → 關鍵字數量
life = get_data("life_table")                   # 生活 → 關鍵字數量
international = get_data("international_table") # 國際 → 關鍵字數量
chian = get_data("chian_table")                 # 大陸 → 關鍵字數量
finance = get_data("finance_table")             # 財經 → 關鍵字數量
cloud = get_data("cloud_table")                 # 雲論 → 關鍵字數量
entertainment = get_data("entertainment_table") # 娛樂 → 關鍵字數量
health = get_data("health_table")               # 健康 → 關鍵字數量
travel = get_data("tourism_table")              # 旅遊 → 關鍵字數量
house = get_data("house_table")                 # 房地產 → 關鍵字數量
sport = get_data("sport_table")                 # 運動 → 關鍵字數量

# 日期
datetime_dt = datetime.datetime.today() # 獲得當地時間
datetime_str = datetime_dt.strftime("%Y-%m-%d")

# 將統計數據寫入 CSV 檔
write_csv(datetime_str, political, society, life ,international ,chian ,finance ,cloud ,entertainment ,health ,travel,house,sport)

## 從資料庫抽取所有關鍵字，更新 jieba 語料庫資料
k1 = get_all_data("political_table")
k2 = get_all_data("society_table")
k3 = get_all_data("life_table")
k4 = get_all_data("international_table")
k5 = get_all_data("chian_table")
k6 = get_all_data("finance_table")
k7 = get_all_data("cloud_table")
k8 = get_all_data("entertainment_table")
k9 = get_all_data("health_table")
k10 = get_all_data("tourism_table")
k11 = get_all_data("house_table")
k12 = get_all_data("sport_table")
k13 = get_all_data("old_table")

keyword_ls = k1+k2+k3+k4+k5+k6+k7+k8+k9+k10+k11+k12+k13
ettoday_ls = list(set(keyword_ls))

tk_ls = []

###### 關鍵字權重分類 #######
for total_keyword in ettoday_ls:
    
    if len(total_keyword) == 1:
        tk = total_keyword + ' 1\n'
        tk_ls += [tk]
        
    elif len(total_keyword) == 2:
        tk = total_keyword + ' 3\n'
        tk_ls += [tk]
        
    elif len(total_keyword) == 3:
        tk = total_keyword + ' 5\n'
        tk_ls += [tk]
        
    else:
        tk = total_keyword + ' 10\n'
        tk_ls += [tk]

content = "".join(tk_ls)
        
with open("/home/cfd888/external_hdd/public_html/temp.check-article.cfd888.info/suggest_keyword.txt","w",encoding="utf-8",errors="ingnor") as keywords:
    keywords.write(content)