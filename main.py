from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Query
import requests
import os


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the Weather API"}

@app.get("/weather")
def get_weather(city: str = Query(..., description="City name")):
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "City not found or API issue"}

    data = response.json()
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    condition = data["weather"][0]["description"]

    return {
        "city": city,
        "temperature": f"{temp} °C",
        "humidity": f"{humidity}%",
        "condition": condition
    }
