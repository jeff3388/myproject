# -*- coding:utf-8 -*- 
from flask import render_template
from jieba.analyse import *
from flask import Flask
import urllib.parse
import itertools
import sqlite3
import jieba

app = Flask(__name__) # 應用程式初始化

# 定義資料庫物件
def get_db(keyword):
    k = ('%' + keyword + '%',)
    try:
        db_keyword_str = ""
        DB = sqlite3.connect('keyword.db')
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

# 測試是否正常啟動
@app.route('/')
def start():
    talk = '啟動成功'
    return talk

# 如果想將arg 傳入所定義好的 function,可以使用以下方法 
@app.route('/article/<article>')
def show_user_profile(article):
    
    #### 解碼成中文字串 ####
    # chinese_word = urllib.parse.unquote(article).replace('未經許可，禁止轉載責任編輯：',"")
    chinese_word = article.replace('.',"").replace('+','').replace('0','').replace('_','').replace('未經許可，禁止轉載責任編輯：',"")

    #### 載入自訂義關鍵字 ####
    file_name = 'suggest_keyword.txt'
    jieba.load_userdict(file_name) 

    #### 載入停用關鍵字 #####
    with open("stop_words.txt","r",encoding='utf-8') as f:
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

    # 重新做關鍵字的排列組合
    k1,k2,k3,k4 = top4_Word_ls[0],top4_Word_ls[1],top4_Word_ls[2],top4_Word_ls[3]
    k_ls = list(itertools.permutations([k1,k2,k3,k4],2))
    word_ls = [] # 12種排列組合的關鍵字
    for i in k_ls:
        word_ls += ["".join(i)]

    word16_ls = word_ls + top4_Word_ls # 16種排列組合的關鍵字

    ## 從資料庫撈出文章關鍵字 ###
    keyWords_ls = []
    for keyword in word16_ls:
        uListStr = get_db(keyword)
        keyWords_ls += [uListStr]

    keyWords = ",".join(keyWords_ls).split(",")
    result = [i for i in keyWords if i not in [""]]
    
    # 若關鍵字如果數量超過10個，則先取15個，再去重複
    if len(result) > 10:
        result = list(set(result[:15]))
        result_str = ",".join(result[:10])
    
    # 若關鍵字數量小於等於10個則直接輸出
    elif len(result) <= 10:
        result_str = ",".join(result)

    return result_str

app.run(debug=True,port=5000) # 正式運作api時 , 請調整回debug=false
                     # port=5000 可以依情況修改, 啟動網址 → http://127.0.0.1:5000(本機端執行，無法從外部拜訪)

