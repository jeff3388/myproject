from flask import Flask
from jieba.analyse import *
import jieba
import urllib.parse

app = Flask(__name__) # 應用程式初始化

@app.route('/')
def start():
    talk = '啟動成功'
    return talk

# 如果想將arg 傳入所定義好的 function,可以使用以下方法 
@app.route('/article/<arg>')
def show_user_profile(arg):
    
    #### 解碼成中文字串 ####
    chinese_word = urllib.parse.unquote(arg).replace('未經許可，禁止轉載責任編輯：',"").replace('.',"")

    #### 載入自訂義關鍵字 ####
    file_name = './suggest_keyword.txt'
    jieba.load_userdict(file_name) 

    #### 載入停用關鍵字 #####
    with open("./stop_words.txt","r",encoding='utf-8') as f:
        stop_word = f.read().replace("\ufeff","").split(",")


    #### 文章斷詞 ####
    seg_list = jieba.cut_for_search(chinese_word) # 搜尋引擎模式
    content = "/".join(seg_list)

    content_ls = content.split("/")
    
    ### 清理冗詞 ###
    correct_word = [ w for w in content_ls if w not in stop_word ]
    article = ",".join(correct_word)

    top4_Word_ls = []

    # 關鍵字權重
    for k,w in extract_tags(article,topK=4,withWeight=True):
        top4_Word_ls += [k]

    words = ",".join(top4_Word_ls)
    return words

app.run(debug=False) # 正式運作api時 , 請調整回debug=false
                     # port=5500 可以依情況修改, 啟動網址 → http://127.0.0.1:5500(本機端執行，無法從外部拜訪)

