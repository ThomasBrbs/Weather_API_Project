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
    return await controller.get_current_weather(request)


@app.post("/weather/forecast")
async def get_weather_forecast(request: ModelRequest):
    return await controller.get_weather_forecast(request)


@app.post("/weather/history")
async def get_weather_history(request: ModelRequest):
    return await controller.get_weather_history(request)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
