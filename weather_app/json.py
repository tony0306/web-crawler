import requests
import json

API_KEY = '78c35360f51186c0c8099c0084b2a919'
CITY = 'Taipei'
URL = f'http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric'

def fetch_weather_data():
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data:", response.text)
        return None

def save_json_to_file(filename):
    data = fetch_weather_data()
    if data:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"JSON data saved to {filename}")
    else:
        print("No data fetched")

# 呼叫函式來保存 JSON 資料到檔案中
save_json_to_file('weather_data.json')

