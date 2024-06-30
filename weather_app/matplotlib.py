import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

API_KEY = '78c35360f51186c0c8099c0084b2a919'
CITY = 'Taipei'
URL = f'http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric'

def fetch_weather_data():
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data")
        return None

def parse_weather_data(data):
    weather_list = data['list']
    parsed_data = []

    for entry in weather_list:
        dt = datetime.fromtimestamp(entry['dt'])
        temp = entry['main']['temp']
        humidity = entry['main']['humidity']
        description = entry['weather'][0]['description']
        parsed_data.append([dt, temp, humidity, description])
    
    return pd.DataFrame(parsed_data, columns=['Date', 'Temperature', 'Humidity', 'Description'])

def save_to_csv(dataframe, filename='weather_data.csv'):
    dataframe.to_csv(filename, index=False)

data = fetch_weather_data()
if data:
    df = parse_weather_data(data)
    save_to_csv(df)
    print("Weather data saved to weather_data.csv")
else:
    print("Failed to retrieve data")
#%%
# 從CSV文件讀取數據
df = pd.read_csv('weather_data.csv')

# 轉換日期欄位為datetime類型
df['Date'] = pd.to_datetime(df['Date'])
# 顯示中文
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  
plt.rcParams['axes.unicode_minus'] = False  
# 繪製溫度變化圖
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Temperature'], marker='o')
plt.title('溫度趨勢')
plt.xlabel('日期')
plt.ylabel('溫度 (°C)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 繪製濕度變化圖
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Humidity'], marker='o', color='orange')
plt.title('濕度趨勢')
plt.xlabel('日期')
plt.ylabel('濕度 (%)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()