# -*- coding:utf-8 -*- 

from flask import render_template
from flask import Flask
from jieba.analyse import *
from flask import request
from flask import Flask
import urllib.parse
import itertools
import sqlite3
import config
import jieba
import csv
import re

app = Flask(__name__) # 應用程式初始化
app.config.from_object(config)

# 定義傳遞的 json format
def json_format(data,status,msg):
    response = {"data":data,"status":status,"msg":[msg]}
    r = str(response)
    return r

# 定義資料庫物件
# @app.route('/keyword/<keyword>')
def get_db(keyword):
    k = ('%' + keyword + '%',)
    try:
        db_keyword_str = ""
        db_path = '/home/cfd888/external_hdd/public_html/temp.check-article.cfd888.info/keyword.db'
        # db_path = 'keyword.db'
        DB = sqlite3.connect(db_path)
        cur = DB.execute('''SELECT * FROM
                                keyword_table 
                                WHERE keyword LIKE (?) ''', k)
        rows = cur.fetchall()
        for row in rows:
            db_keyword_str += str(row[0]) + ","
            DB.close()

        return db_keyword_str

    except Exception as err:

        return err

# 讀取關鍵字數據
def search_data(date):
    with open(r'C:\Users\CFD029\Desktop\output.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if date in row:
                date = row[0] # 日期
                political = row[1] # 政治
                society = row[2] # 社會
                life = row[3] # 生活
                international = row[4] # 國際
                chian = row[5] # 大陸
                finance = row[6] # 財經
                cloud = row[7] # 雲論
                entertainment = row[8] # 財經
                health = row[9] # 國際
                travel = row[10] # 大陸
                house = row[11] # 財經
                sport = row[12] # 財經

            else:
                date, political, society, life ,international ,chian ,finance ,cloud ,entertainment ,health ,travel,house,sport = date,"0","0","0","0","0","0","0","0","0","0","0","0"
                      
    return date, political, society, life ,international ,chian ,finance ,cloud ,entertainment ,health ,travel,house,sport

# 啟動渲染的 html page 
@app.route('/')
def start():
    return render_template('hello.html')

# 撈取關鍵字數量報告
@app.route('/keyword-date', methods=['GET', 'POST'])
def date():
    if request.method == 'GET':
        return render_template('keyword_quantity.html')
        
    else:
        date_time = request.form.get('date') # 取得日期
        date, political, society, life ,international ,chian ,finance ,cloud ,entertainment ,health ,travel,house,sport = search_data(date_time) # 讀取 CSV 檔的數據
        return render_template('keyword_quantity.html', political=political # 政治
                                                      , society=society # 社會
                                                      , travel=travel # 旅遊
                                                      , life=life # 生活
                                                      , international=international # 國際
                                                      , chian=chian # 大陸
                                                      , finance=finance # 財經
                                                      , date = date # 日期
                                                      , cloud = cloud # 雲論
                                                      , entertainment = entertainment # 娛樂
                                                      , health = health # 健康
                                                      , house = house # 房地產
                                                      , sport = sport # 運動
                                                      )

@app.route("/post_submit", methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # 透過 request.values['article'] 的方法取得 values
        article = request.values['article']
        chinese_word = article.replace('.',"").replace('+','').replace('0','').replace('_','').replace('未經許可，禁止轉載責任編輯：',"")

        #### 載入自訂義關鍵字 ####
        file_name = '/home/cfd888/external_hdd/public_html/temp.check-article.cfd888.info/suggest_keyword.txt'
        # file_name = 'suggest_keyword.txt'
        jieba.load_userdict(file_name) 

        #### 載入停用關鍵字 #####
        stop_word_path = "/home/cfd888/external_hdd/public_html/temp.check-article.cfd888.info/stop_words.txt"
        # stop_word_path = "stop_words.txt"
        with open(stop_word_path,"r",encoding='utf-8') as f:
            stop_word = f.read().replace("\ufeff","").split(",")
            
        #### 文章斷詞 ####
        seg_list = jieba.cut_for_search(chinese_word, HMM=True) # 搜尋引擎模式
        content = "/".join(seg_list)

        content_ls = content.split("/")

        ### 清理冗詞 ###
        correct_word = [ w for w in content_ls if w not in stop_word ]
        article = ",".join(correct_word)

        top4_Word_ls = []

        # 關鍵字權重
        for k,w in extract_tags(article,topK=4,withWeight=True):
            top4_Word_ls += [k]
        try:
            # 重新做關鍵字的排列組合
            k1,k2,k3,k4 = top4_Word_ls[0],top4_Word_ls[1],top4_Word_ls[2],top4_Word_ls[3]
            k_ls = list(itertools.permutations([k1,k2,k3,k4],2))

            # 模糊比對關鍵字是否存在文章
            exist_string_ls = [] 
            for j in k_ls:
                a,b = j[0],j[1]
                m = re.match('.*' + a + '.*' + b, article)
                if m != None:
                    s = a+b
                    exist_string_ls += [s]

            exist_string_ls = exist_string_ls + top4_Word_ls # 加入高權重4組詞彙

            ## 從資料庫撈出文章關鍵字 ###
            keyWords_ls = []
            for keyword in exist_string_ls:
                db_keyword_str = get_db(keyword)
                keyWords_ls += [db_keyword_str]
            
            keyWords = ",".join(keyWords_ls).split(",")
            result = [i for i in keyWords if i not in [""]]
            
            # 若關鍵字如果數量超過10個，則先取15個，再去重複
            if len(result) > 10:
                result = list(set(result[:11]))
                data = result
                status = "true"
                msg = "success"
                result_str = json_format(data,status,msg)
            
            # 若關鍵字數量小於等於10個則直接輸出
            elif len(result) <= 10:
                data = result
                status = "true"
                msg = "success"
                result_str = json_format(data,status,msg)

            elif result == 0:
                data = "None"
                status = "false" 
                msg = "或許您的文章長度不夠，導致無法成功解析關鍵字","或許資料庫無此文章關鍵字，導致無法回傳關鍵字"
                result_str = json_format(data,status,msg)

            return result_str

        except Exception as status:
            data = "None"
            msg = "或許您的文章長度不夠，導致無法成功解析關鍵字","或許資料庫無此文章關鍵字，導致無法回傳關鍵字"
            result_str = json_format(data,status,msg)

            return result_str

    return render_template("post_submit.html")

app.run(debug=True,port=5000) # 正式運作api時 , 請調整回debug=false
                              # port=5000 可以依情況修改, 啟動網址 → http://127.0.0.1:5000(本機端執行，無法從外部拜訪)
