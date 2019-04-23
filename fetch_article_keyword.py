# -*- coding:utf-8 -*- 

from jieba.analyse import *
import jieba
import itertools
import sqlite3
import time

db_name = r'C:\Users\CFD029\Desktop\article.db'
con = sqlite3.connect(db_name)
c = con.cursor() # 建立連線物件

# 搜尋關鍵字
def get_data():
    
    key_ls = []
    
    # （%）代表零個、一個或多個數字或字串
    # 底線（_）代表一個、單一的數字或字串
    
    with con:
        c.execute('''SELECT * FROM
                     article_table 
                     ORDER BY article ''')
        
        rows = c.fetchall()
        for row in rows:
            key_ls += [row[0]]
            
    return key_ls
            
key_ls = get_data()

for article in key_ls:
    try:
        
        chinese_word = article.replace('.',"").replace('+','').replace('0','').replace('_','').replace('未經許可，禁止轉載責任編輯：',"")

        #### 載入自訂義關鍵字 ####
        file_name = r'C:\Users\CFD029\Desktop\linux_google_keyword\suggest_keyword.txt'
        jieba.load_userdict(file_name) 

        #### 載入停用關鍵字 #####
        with open(r"C:\Users\CFD029\Desktop\linux_google_keyword\stop_words.txt","r",encoding='utf-8') as f:
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
        word16_str = ",".join(word16_ls)
        with open(r'C:\Users\CFD029\Desktop\article_keywords.txt','a',encoding='utf-8',errors='ingnor') as f:
            f.write(word16_str)
            
    except Exception as e:
        print(e)