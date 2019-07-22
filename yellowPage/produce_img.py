import matplotlib.pyplot as plt
import pandas as pd
import datetime

# 生成總量趨勢圖表圖片

df = pd.read_csv('/jojo/yellow_page/yellow_page_total_trend.csv')
y_numbers = df.loc[0:,'number']
x_lable = df.loc[0:,'date']

y_numbers = y_numbers.values
y_numbers = list(y_numbers)

x_lable = x_lable.values
x_lable = list(x_lable)

# 製作圖表

plt.style.use('ggplot') # 進行風格美化
plt.figure(figsize=(20,10)) # 控制顯示圖片的布局大小
plt.bar(x_lable ,y_numbers ,label = 'Daily data' ,fc = '#5555FF' ,width = 0.45) # plt.bar(標籤 list, 資料參數 list, 圖片右上角標籤 , 柱狀體色碼)
plt.legend() # 要使用label要加這行

plt.title("Data statistic") # 數據統計
plt.xlabel("date") # 日期
plt.ylabel("data amount") # 數據總量
plt.savefig('/jojo/yellow_page/histogram.jpg')