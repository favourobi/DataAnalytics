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
