# -*- coding:utf-8 -*- 
import sqlite3

db_name = r'C:\Users\CFD029\Desktop\keyword.db'
con = sqlite3.connect(db_name)
c = con.cursor() # 建立連線物件

# 確認表格是否存在，不存在則重新建立
def db_table():
    c.execute('''CREATE TABLE IF NOT EXISTS 
                 keyword_table ( keyword TEXT PRIMARY KEY
                                 )''')

# 插入多筆資料
def insert_many(word):
    try:
        with con:
                c.executemany('''INSERT INTO keyword_table 
                                 (keyword) VALUES (?)''',(word))
                con.commit() # 提交資料
    except:
        pass
        
# 單筆資料
def insert_data(verification):
    with con:
        c.execute('INSERT INTO keyword_table (keyword) VALUES (?)',[verification])
        con.commit() # 提交資料

# 搜尋關鍵字
def get_data(keyword):
    
    key_ls = []
    
    # （%）代表零個、一個或多個數字或字串
    # 底線（_）代表一個、單一的數字或字串
    
    k = ('%' + keyword + '%',)
    with con:
        c.execute('''SELECT * FROM
                     keyword_table 
                     WHERE keyword LIKE (?) ''', k)
        
        rows = c.fetchall()
        for row in rows:
            key_ls += [row[1]]
            
    return key_ls