from dotenv import load_dotenv
import os
import requests
import math

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


def get_weather(city_name):
    # TODO!: Do an actual API Call
    print("🔨 Tool Called: get_weather for", city_name)
    
    url = f"https://api.openweathermap.org/data/2.5/weather?units=metric&q={city_name}&appid={WEATHER_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        parsed_response = response.json()
        # print(math.floor(parsed_response["main"]["temp"])) 
        return f"The weather in {city_name} is {math.floor(parsed_response["main"]["temp"])}."
    return "Something went wrong"

if __name__ == "__main__":
    get_weather("delhi")