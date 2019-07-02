# _*_ coding:utf-8 _*_

# 更新 output csv 檔案

import datetime
import obj

# 獲取資料庫新聞關鍵字數量
political = obj.get_data("political_table")         # 政治 → 關鍵字數量
society = obj.get_data("society_table")             # 社會 → 關鍵字數量
life = obj.get_data("life_table")                   # 生活 → 關鍵字數量
international = obj.get_data("international_table") # 國際 → 關鍵字數量
chian = obj.get_data("chian_table")                 # 大陸 → 關鍵字數量
finance = obj.get_data("finance_table")             # 財經 → 關鍵字數量
cloud = obj.get_data("cloud_table")                 # 雲論 → 關鍵字數量
entertainment = obj.get_data("entertainment_table") # 娛樂 → 關鍵字數量
health = obj.get_data("health_table")               # 健康 → 關鍵字數量
travel = obj.get_data("tourism_table")              # 旅遊 → 關鍵字數量
house = obj.get_data("house_table")                 # 房地產 → 關鍵字數量
sport = obj.get_data("sport_table")                 # 運動 → 關鍵字數量

# 日期
datetime_dt = datetime.datetime.today() # 獲得當地時間
datetime_str = datetime_dt.strftime("%Y-%m-%d")

# 將統計數據寫入 CSV 檔
obj.write_csv(datetime_str, political, society, life ,international ,chian ,finance ,cloud ,entertainment ,health ,travel,house,sport)

## 從資料庫抽取所有關鍵字，更新 jieba 語料庫資料
k1 = obj.get_all_data("political_table")
k2 = obj.get_all_data("society_table")
k3 = obj.get_all_data("life_table")
k4 = obj.get_all_data("international_table")
k5 = obj.get_all_data("chian_table")
k6 = obj.get_all_data("finance_table")
k7 = obj.get_all_data("cloud_table")
k8 = obj.get_all_data("entertainment_table")
k9 = obj.get_all_data("health_table")
k10 = obj.get_all_data("tourism_table")
k11 = obj.get_all_data("house_table")
k12 = obj.get_all_data("sport_table")
k13 = obj.get_all_data("old_table")

keyword_ls = k1+k2+k3+k4+k5+k6+k7+k8+k9+k10+k11+k12+k13
ettoday_ls = list(set(keyword_ls))

tk_ls = []

###### 更新 jieba 語料庫關鍵字權重分類 #######
for total_keyword in ettoday_ls:
    
    if len(total_keyword) == 1:
        tk = total_keyword + ' 1'
        tk_ls += [tk]
        
    elif len(total_keyword) == 2:
        tk = total_keyword + ' 3'
        tk_ls += [tk]
        
    elif len(total_keyword) == 3:
        tk = total_keyword + ' 5'
        tk_ls += [tk]
        
    else:
        tk = total_keyword + ' 10'
        tk_ls += [tk]

content = "\n".join(tk_ls)
        
with open("/home/cfd888/external_hdd/public_html/temp.check-article.cfd888.info/suggest_keyword.txt","w",encoding="utf-8") as keywords:
    keywords.write(content)
