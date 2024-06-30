from flask import Flask, render_template
import pandas as pd
import requests
from datetime import datetime
#%%在不同的環境中能夠正確地定位和載入這些資源，無需你明確地指定路徑。

app = Flask(__name__)

API_KEY = '78c35360f51186c0c8099c0084b2a919'
CITY = 'Taipei'
DISPLAY_CITY = '台北'
URL = f'http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric'
#%%天氣描述翻譯字典

weather_descriptions = {
    'clear sky': '晴朗',
    'few clouds': '少雲',
    'scattered clouds': '疏雲',
    'broken clouds': '多雲',
    'overcast clouds': '陰天',
    'light rain': '小雨',
    'moderate rain': '中雨',
    'heavy intensity rain': '大雨',
    'thunderstorm': '雷陣雨',
    'snow': '雪',
    'mist': '霧'
}
#%%抓取天氣資料，然後將資料轉換成 JSON 格式返回

def fetch_weather_data():
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    else:
        print("獲取數據錯誤:", response.text)  # 調試信息：打印錯誤信息
        return None
#%%
def translate_description(description):
    return weather_descriptions.get(description, description)
#%%用於解析從天氣 API 中獲取的 JSON 格式資料 data
def parse_weather_data(data):
    weather_list = data['list']
    parsed_data = []

    for entry in weather_list:
        dt = datetime.fromtimestamp(entry['dt'])
        temp = entry['main']['temp']
        humidity = entry['main']['humidity']
        description = entry['weather'][0]['description']
        translated_description = translate_description(description)
        parsed_data.append({'日期': dt, '溫度': temp, '濕度': humidity, '描述': translated_description})
    
    return parsed_data
#%%轉換為 HTML 表格格式，並且傳遞給模板引擎用於在網頁上顯示
@app.route('/')
def index():
    data = fetch_weather_data()
    if data:
        weather_data = parse_weather_data(data)
        df = pd.DataFrame(weather_data)
        return render_template('index.html', city=DISPLAY_CITY, tables=[df.to_html(classes='data', header="true", index=False)], titles=df.columns.values)
    else:
        return "獲取天氣數據失敗"
#%%確保 Flask 應用在直接運行時能夠正確地啟動和運行
if __name__ == '__main__':
    app.run(debug=False)