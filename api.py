from fastapi import FastAPI, HTTPException
from typing import Dict
from src.models.ModelRequest import ModelRequest
from src.controllers.WeatherController import WeatherController
from src.services.WeatherService import WeatherService

app = FastAPI(title="API")


weather_service = WeatherService()
controller = WeatherController(weather_service)


@app.post("/weather/current")
async def get_current_weather(request: ModelRequest):
    print(request)
    return await controller.get_current_weather(request)
