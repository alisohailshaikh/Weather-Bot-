from flask import Flask, request,json,jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

WEATHER_API_KEY = 'f3bb13fb2535d7caf1b4fdacd56b6318'
WEATHER_API_URL = 'http://api.weatherapi.com/v1'


def fetch_weather_forecast(city, date):
    coords = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={WEATHER_API_KEY}")
    coords = coords.json()
    lon = coords[0]["lon"]
    lat = coords[0]["lat"]
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    new_date = date_obj + timedelta(days=7)
    end_date = new_date.strftime("%Y-%m-%d")
    endpoint = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,daylight_duration,sunshine_duration,precipitation_sum,rain_sum,showers_sum,wind_speed_10m_max&timezone=GMT&start_date={date}&end_date={end_date}"
    data = requests.get(endpoint)
    data = data.json()
    data = data["daily"]
    weather_info = (f"City: {city}\n")
    for i in range(0,8):
        daylight = data["daylight_duration"][i]
        prep = data["precipitation_sum"][i]
        max_temp = data["temperature_2m_max"][i]
        rain = data["rain_sum"][i]
        shower = data["showers_sum"][i]
        sun = data["sunshine_duration"][i]
        min_temp = data["temperature_2m_min"][i]
        w_date = data["time"][i]
        wind = data["wind_speed_10m_max"][i]
        temp = (f"\nDate: {w_date}\n"
                f"Min Temperature: {min_temp}°C\n"
                    f"Max Temperature: {max_temp}°C\n"
                    f"Wind Speed: {wind} km/h\n"
                    f"Daylight Duration: {daylight}\n"
                    f"Sun Duration: {sun}\n"
                    f"Precipitation Sum: {prep}\n"
                    f"Rain Sum: {rain}\n"
                    f"Shower Sum: {shower}\n"
                    f"\n-\n"

        )
        
        weather_info = weather_info+temp



    return jsonify({"weather": weather_info})

def fetch_weather(city):
    endpoint = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&cnt=10&mode=json&units=metric&appid={WEATHER_API_KEY}"
    data = requests.get(endpoint)
    data = data.json()

    entry = data['list'][0]
    date_time = entry['dt_txt']
    temperature = entry['main']['temp']
    temperature_min = entry['main']['temp_min']
    temperature_max = entry['main']['temp_max']
    humidity = entry['main']['humidity']
    weather_description = entry['weather'][0]['description']
    wind_speed = entry['wind']['speed']
    wind_gust = entry['wind']['gust']
    weather_info = (f"City: {city}\n"
                    f"Date and Time: {date_time}\n"
                    f"Temperature: {temperature}°C\n"
                    f"Min Temperature: {temperature_min}°C\n"
                    f"Max Temperature: {temperature_max}°C\n"
                    f"Humidity: {humidity}%\n"
                    f"Weather: {weather_description}\n"
                    f"Wind Speed: {wind_speed} m/s\n"
                    f"Wind Gust: {wind_gust} m/s")

    return jsonify({"weather": weather_info})



@app.route('/webhook.json', methods=['POST'])
def webhook():
    data = request.get_json()
    city = data['city']
    print(city)
    date = data.get('date')
    print(date)
    if date:
        data = fetch_weather_forecast(city,date)
    else:
        data = fetch_weather(city)
    return data

if __name__ == '__main__':
    app.run(port=5000)
