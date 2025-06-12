'''
import requests
import urllib.request as k

API_KEY1 = "a53cdae913a5e85c56ee542b33bedccd"
API_KEY2 = "8cc318f610b994a0058803f7f8e27ee1"
CITY = "London"
BASE_URL = "http://api.openweathermap.org/geo/1.0/direct?q=London&limit=5&appid=a53cdae913a5e85c56ee542b33bedccd"

params = {
    "q": CITY,
    "appid": API_KEY1,
    "units": "metric"  # Use 'imperial' for Fahrenheit
}

response = requests.get(BASE_URL, params=params)


data = response.json()
for location in data:
    name = location.get("name")
    lat = location.get("lat")
    lon = location.get("lon")
    
    
    #print(f"{name}: Latitude = {lat}, Longitude = {lon}")

path = f"api.openweathermap.org/data/2.5/forecast?{lat}&{lon}&appid={API_KEY2}"
reply = k.urlopen(path,str,1000)
data1 = reply.json()
'''   


import requests

def get_weather_openweathermap(city, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    # Parameters: city name, units (metric = °C), and API key
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        print(f"Weather in {city}: {weather}")
        print(f"Temperature: {temperature}°C")
        print(f"Feels like: {feels_like}°C")
        print(f"Humidity: {humidity}%")
        print(f"Wind speed: {wind_speed} m/s")
    else:
        print("Failed to retrieve data:", response.status_code, response.text)

# Example usage
api_key = "a53cdae913a5e85c56ee542b33bedccd"  # Replace this with your real API key
get_weather_openweathermap("Lagos", api_key)
