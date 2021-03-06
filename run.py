# -*- coding:utf-8 -*- 
from decimal import getcontext, Decimal
from flask import render_template
from datetime import timedelta
from flask import Flask
from jieba.analyse import *
from flask import request
from flask import Flask
import pandas as pd
import numpy as np
import urllib.parse
import portalocker
import itertools
import sqlite3
import datetime
import config
import jieba
import time
import csv
import re
import os

app = Flask(__name__) # 應用程式初始化
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=2) 
app.config.from_object(config)

path = '/home/cfd888/external_hdd/public_html/temp.check-article.cfd888.info'
# path = '.'
# 定義傳遞的 json format
def json_format(data,hide,status,msg):
    response = {"data":data,"hide":hide,"status":status,"msg":[msg]}
    r = str(response)
    return r

# 定義資料庫物件
# @app.route('/keyword/<keyword>')
def get_db(keyword):
    k = ('%' + keyword + '%',)
    try:
        db_keyword_str = ""
        db_path = path + '/keyword.db'
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

# 讀取 txt 檔內的 url，調用完畢即刪除
def read_url():
    with open(path + '/yellow_url.txt', 'r',encoding='utf-8') as f:
        fi = f.read().split(";")
        url_ls = fi[0:1]
        replace_url = ";".join(fi[1:])

    with open(path + '/yellow_url.txt', 'w',encoding='utf-8') as f:
        f.write(replace_url)
    
    url_str = ";".join(url_ls)

    return url_str

# 計算抓回數據的總量
def caculation_total(date_time):
    try:
        bond = pd.read_csv(path +'/yellow_page_total_data.csv', index_col="date") # 選擇欄位
        total = bond.values.tolist()
        data = bond.loc[date_time].values.tolist()

        total_data = str(len(total)) # 數據總量
        int_data = len(data) # 選擇日期所帶出的數據量
        date_time_data = str(len(data)) # 選擇日期所帶出的數據量
        hr_total = int_data / 24 # 平均每小時數量
        min_total = int_data /1440 # 平均每分鐘數量
        
        hr_total = Decimal(str(hr_total)).quantize(Decimal('0.00')) # 取到小數點第2位
        min_total = Decimal(str(min_total)).quantize(Decimal('0.00')) # 取到小數點第2位

        return total_data, date_time_data, hr_total, min_total

    except:
        # if index csv file fail
        bond = pd.read_csv(path +'/yellow_page_total_data.csv', index_col="date") # 選擇欄位
        total = bond.values.tolist()
        total_data = str(len(total))

        data_total, hr_total, min_total = '0','0','0'
        return total_data, data_total, hr_total, min_total

# 讀取關鍵字數據(ettoday)
def search_data(date_time):
    try:
        bond = pd.read_csv(path + '/output.csv', index_col="date")
        date = bond.loc[date_time]
        date_array = np.array(date) # 先轉換 numpy array
        date_list = date_array.tolist() # 使用 tolist() 方法轉換成 list 格式

        return date_time, date_list

    except:
        date_list = ["0","0","0","0","0","0","0","0","0","0","0","0"]

        return date_time, date_list

#######################################################################################################
# 啟動渲染的 html page 
@app.route('/')
def start():
    return render_template('hello.html')

# 派發任務 - 黃頁任意門 url api 
@app.route('/yp-url')
def yellowPage_url():
    url_str = read_url()

    return url_str

# 測試用寫入資料的 API
@app.route("/test_csv", methods=['GET', 'POST'])
def test_csv():
    if request.method == 'POST':
        # 透過 request.values['writecsv'] 的方法取得 values
        write_csv = request.values['test'] # write_csv的字串型態='公司,na,電話,na,地址,區域,na,na,na,na,種類'
        ls = write_csv.split(';')
        ls = [h for h in ls if h not in [""]]
        limit = 1 # 每組人數
        table = [ls[i:i + limit] for i in range(0, len(ls), limit)]
        try:
            with open(path + '/test.csv', 'a', newline='' ,encoding='utf-8') as csvfile:
                portalocker.lock(csvfile, portalocker.LOCK_EX) # 文件上瑣，存取完畢才解瑣
                writer = csv.writer(csvfile)
                writer.writerows(table)
        except Exception as e:
                time.sleep(5)
                try:
                    with open(path +'/test.csv', 'a', newline='', encoding='utf-8') as csvfile:
                        portalocker.lock(csvfile, portalocker.LOCK_EX) #  文件上瑣，存取完畢才解瑣
                        writer = csv.writer(csvfile)
                        writer.writerows(table)
                except Exception as e:
                    print(e)
        return "success"
    else:
        return render_template('test.html')

# 寫入資料 web393 的 API
@app.route("/web393", methods=['GET', 'POST'])
def web393():
    file_name = '/web393.txt'
    if request.method == 'POST':
        # 透過 request.values['writecsv'] 的方法取得 values
        web_str = request.values['web'] # write_csv的字串型態='公司,na,電話,na,地址,區域,na,na,na,na,種類'

        try:
            with open(path + file_name , 'a', newline='' ,encoding='utf-8') as txtfile:
                portalocker.lock(txtfile, portalocker.LOCK_EX) # 文件上瑣，存取完畢才解瑣
                txtfile.write(web_str)
                
        except Exception as e:
                print(e)
                time.sleep(5)
                try:
                    with open(path + file_name , 'a', newline='' ,encoding='utf-8') as txtfile:
                        portalocker.lock(txtfile, portalocker.LOCK_EX) # 文件上瑣，存取完畢才解瑣
                        txtfile.write(web_str)
                except Exception as e:
                    print(e)

        return "success"
    else:
        return render_template('web393.html')

# 寫入資料的API
@app.route("/write_csv", methods=['GET', 'POST'])
def write_csv():
    if request.method == 'POST':
        # 透過 request.values['writecsv'] 的方法取得 values
        write_csv = request.values['string'] # write_csv的字串型態='公司,na,電話,na,地址,區域,na,na,na,na,種類'
        ls = write_csv.split(';')
        ls = [h for h in ls if h not in [""]]
        limit = 12 # 每組人數
        table = [ls[i:i + limit] for i in range(0, len(ls), limit)]
        try:
            with open(path + '/yellow_page_total_data.csv', 'a', newline='' ,encoding='utf-8') as csvfile:
                portalocker.lock(csvfile, portalocker.LOCK_EX) # 文件上瑣，存取完畢才解瑣
                writer = csv.writer(csvfile)
                writer.writerows(table)
        except Exception as e:
                time.sleep(5)
                try:
                    with open(path +'/yellow_page_total_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
                        portalocker.lock(csvfile, portalocker.LOCK_EX) #  文件上瑣，存取完畢才解瑣
                        writer = csv.writer(csvfile)
                        writer.writerows(table)
                except Exception as e:
                    print(e)
        return "success"
    else:
        return render_template('write_csv.html')

# 撈取關鍵字數量報告(ETtoday)
@app.route('/keyword-date', methods=['GET', 'POST'])
def keyword_date():
    # 如果直接url請求的話，則直接顯示 html page
    if request.method == 'GET':
        return render_template('keyword_quantity.html')
    
    # 不然則無條件直接取表格 attribute 的 values
    else:
        date_time = request.form.get('date') # 取得日期
        date_time, date_list = search_data(date_time) # 讀取 CSV 檔的數據
        return render_template('keyword_quantity.html', political = date_list[0] # 政治
                                                      , society = date_list[1] # 社會
                                                      , life = date_list[2] # 生活
                                                      , international=date_list[3] # 國際
                                                      , chian = date_list[4] # 大陸
                                                      , finance = date_list[5] # 財經
                                                      , cloud = date_list[6] # 雲論
                                                      , entertainment = date_list[7] # 娛樂
                                                      , health = date_list[8] # 健康
                                                      , travel= date_list[9] # 旅遊
                                                      , house = date_list[10] # 房地產
                                                      , sport = date_list[11] # 運動
                                                      , date = date_time # 日期
                                                      )

# 撈取黃頁數據
@app.route('/yellow-page', methods=['GET', 'POST'])
def yellow_page():
    # 如果直接url請求的話，則直接顯示 html page
    if request.method == 'GET':
        return render_template('yellow_page.html')
    
    # 不然則無條件直接取表格 attribute 的 values
    else:
        date_time = request.form.get('date') # 取得日期
        total = caculation_total(date_time) # 讀取 CSV 檔的數據
        return render_template('yellow_page.html', total_data = total[0] # 數據總量
                                                 , data_total = total[1] # 選擇日期所帶出的數據量
                                                 , hr_total = total[2] # 平均每小時數量
                                                 , min_total = total[3] # 平均每分鐘數量
                                                 , date = date_time # 日期
                                                )


@app.route("/post_submit", methods=['GET', 'POST'])
def post_submit():
    if request.method == 'POST':
        # 透過 request.values['article'] 的方法取得 values
        article = request.values['article']
        chinese_word = article.replace('.',"").replace('+','').replace('0','').replace('_','').replace('未經許可，禁止轉載責任編輯：',"").replace('\n','')

        #### 載入自訂義關鍵字 ####
        file_name = path + '/suggest_keyword.txt'
        jieba.load_userdict(file_name)

        #### 載入停用關鍵字 #####
        stop_word_path = path + "/stop_words.txt"
        with open(stop_word_path,"r",encoding='utf-8') as f:
            stop_word = f.read().replace("\ufeff","").split(",")
            
        #### 文章斷詞 ####
        seg_list = jieba.cut_for_search(chinese_word, HMM=True) # 搜尋引擎模式
        content = "/".join(seg_list)

        content_ls = content.split("/")

        ### 清理冗詞 ###
        correct_word = [ w for w in content_ls if w not in stop_word ]
        article = ",".join(correct_word)

        top6_Word_ls = [] # 前10名關鍵字

        # 保留權重排名前10名的關鍵字
        for k,w in extract_tags(article,topK=10,withWeight=True):
            top6_Word_ls += [k]

        top6_ls = list(itertools.permutations(top6_Word_ls,2))

        # 留長尾去短尾關鍵字 ex: [蔡英文,英文] 只保留 [蔡英文]
        test = []
        for i in top6_ls:
            m1 = re.findall(i[0],i[1])
            if m1 != []:
                m1 = "".join(m1)
                test += [m1]

        f_ls = [u for u in top6_Word_ls if u not in test] # 去除相似關鍵字
        top4_Word_ls = f_ls[:4]
        top8_Word_ls = f_ls[:8]

        try:
            # 重新做關鍵字的排列組合
            k1,k2,k3,k4 = top4_Word_ls[0],top4_Word_ls[1],top4_Word_ls[2],top4_Word_ls[3]
            k_ls = list(itertools.combinations([k1,k2,k3,k4],2)) # ex : [('1', '2'), ('1', '3'), ('1', '4'), ('2', '3'), ('2', '4'), ('3', '4')]
            
            # 模糊比對關鍵字是否存在文章
            exist_string_ls = [] 
            for j in k_ls:
                a,b = j[0],j[1]
                m = re.match('.*' + a + '.*' + b, article)
                if m != None:
                    s = a +" "+ b
                    exist_string_ls += [s]

            exist_string_ls = exist_string_ls + top4_Word_ls # 加入高權重4組詞彙

            if len(exist_string_ls) <= 10:
                data = exist_string_ls
                hide = top8_Word_ls
                status = "true"
                msg = "success"
                result_str = json_format(data,hide,status,msg)
            
            elif len(exist_string_ls) > 10:
                data = exist_string_ls[:11]
                hide = top8_Word_ls
                status = "true"
                msg = "success"
                result_str = json_format(data,hide,status,msg)

            # 如果關鍵字數量等於 0 的情況
            elif len(exist_string_ls) == 0:
                data = "None"
                status = "false" 
                msg = "The number of keywords parsed is zero"
                result_str = json_format(data,hide,status,msg)

            return result_str

        except Exception as msg:
            data = "None"
            hide = "None"
            status = "false"
            result_str = json_format(data,hide,status,msg)

            return result_str

    return render_template("post_submit.html") # 將 result_str 回傳到 post_submit.html 此頁面

app.run(debug=True,port=5000) # 正式運作api時 , 請調整回debug=false
                              # port=5000 可以依情況修改, 啟動網址 → http://127.0.0.1:5000(本機端執行，無法從外部拜訪)
