# -*- coding:utf-8 -*- 

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from flask import Flask
import requests
import random

app = Flask(__name__) # 應用程式初始化

@app.route('/')
def start():
    talk = '啟動成功'
    return talk

# 如果想將arg 傳入所定義好的 function,可以使用以下方法 
@app.route('/article/<keyword>')
def search_keyword(keyword):
    ua = UserAgent()
    user_agent = ua.chrome
    arg = ['nvOmXM7sOrnfmAXq96yQDA','avSmXJj-BYGImAX8wY2ICA','Nd6mXJuOFsSD8gXi0IDACQ','avSmXJj-BYGImAX8wY2ICA',
           'JPWmXIqVOM6kmAWGoY3ABg','hPWmXL2dM-22mAXr_4uIBg','tPemXLGYL4G2mAXyl5uADQ','efemXJfTELHFmAWA2oLwBg',
           't_emXMjfMOatmAWn-7Uo','zPemXMT4FoGVr7wP8-WnYA','5femXLDcJdaMr7wPx9arkAw','EPimXMvRIp-Qr7wP2cqbqAU',
           'MvimXJflA4O9mAWFpLdg','NvimXM-IFfuVr7wPsZw4','0_imXMrUFqyzmAXLrKewCg','8fimXJC_Dqm0mAWPmbHwAw',
           'CPmmXL_ABqWkmAXf-oHgBQ','IfmmXMy9OqmUr7wPnoaGuAc','QfmmXJyGOoKymAXIpo6wCw','V_mmXLn0GrKSr7wPlquo8Ag',
           'bfmmXL-aONuIr7wP9cKD0Ak','iZ6qXM7BH4uB8wW7qLzoBw','q56qXOzqNYy58QXmnYigCQ','yp6qXK6FEMf88AX56omoCA',
           '7Z6qXPesIMmf8QXn_Zz4Dg','DZ-qXLzMM4v08AWntor4Dg','LZ-qXKvVI8bW8QWrtZo4','Qp-qXO3HOMfS8QWa-bwY',
           'J6OqXOK4J4G8mAXt3qToDg','UKOqXJqWIJ2Sr7wPhoeG8AU','TKOqXP3AHMiKr7wP0bWx4AI','gqOqXJzoCKWkmAWjt6eoBw',
           'Db-qXOeDNpCUmAWQsoeADw','Jb-qXO-JAsWJmAXd0IL4Cg','Rr-qXNCqGYnW0gS0kpngCw','Wb-qXPeOJrPUmAXP17rYCg',
           'aL-qXMHhK6WxmAXUirnYDw','e7-qXJugN8um0wSDppHAAQ','pL-qXNPwH5uFr7wP_7uLYA','tr-qXOmOKqOJmAXX0r-gBg',
           '87-qXPfqHeq4mAXsrL2QBw','JcCqXPjOIcmJmAWmnIrICA','OMCqXNGVGMLFmAWa_pPwBA','R8CqXObpEZ6Vr7wPwMSwmAk',
           'WsCqXJvECaWPr7wPztiQiAs','cMCqXPWdAouUr7wPq6OhkAo','i8CqXImvBYiTr7wP9oOs0A0','nsCqXMbKJ_CbmAXr15-YCA']
            
    argument = random.choice(arg)
    headers = {'alt-svc': 'quic=":443"; ma=2592000; v="46,44,43,39"',
               'cache-control': 'no-cache, must-revalidate',
               'content-encoding': 'br',
               'pragma': 'no-cache',
               'server': 'gws',
               'status': '200',
               'strict-transport-security': 'max-age=31536000',
               'content-type': 'application/json; charset=UTF-8',
               'x-frame-options': 'SAMEORIGIN',
               'x-xss-protection': '0',
               'user-agent': user_agent
             }
    url = 'https://www.google.com.tw/search?source=hp&ei=' + argument + '&q='+ keyword + '&btnK=Google+搜尋&oq='+ keyword                                                       
                                                        
    html = requests.get(url=url,headers=headers)
    html = html.content
    soup = BeautifulSoup(html, 'html.parser') 
    key_class = soup.find_all("p", attrs={"class": "nVcaUb"})

    keyword_ls = []
    for i in key_class:
        i = i.text
        keyword_ls += [i]

    keyword_str = ",".join(keyword_ls)
    return keyword_str

app.run(debug=False) # 正式運作api時 , 請調整回debug=false
                     # port=5500 可以依情況修改, 啟動網址 → http://127.0.0.1:5500(本機端執行，無法從外部拜訪)
