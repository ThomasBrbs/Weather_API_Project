from fastapi.responses import JSONResponse
from src.models.ModelRequest import ModelRequest 

class WeatherController:
    def __init__(self, service):
        self.service = service

    async def get_current_weather(self, request: ModelRequest):
        city = request.city.lower()
        if not city:
            return JSONResponse(status_code=400, content={"error": "City parameter is required"})

        weather_data = await self.service.get_current_weather(city)
        if not weather_data:
            return JSONResponse(status_code=404, content={"error": "City not found"})

        return JSONResponse(content=weather_data)


    async def get_weather_forecast(self, request: ModelRequest):
        city = request.city.lower()
        if not city:
            return JSONResponse(status_code=400, content={"error": "City parameter is required"})

        forecast_data = await self.service.get_weather_forecast(city)
        if not forecast_data:
            return JSONResponse(status_code=404, content={"error": "City not found"})

        return JSONResponse(content=forecast_data)

    async def get_weather_history(self, request: ModelRequest):
        city = request.city.lower()
        days = request.days if hasattr(request, "days") else 7  # par défaut 7 jours

        if not city:
            return JSONResponse(status_code=400, content={"error": "City parameter is required"})
        if days <= 0:
            return JSONResponse(status_code=400, content={"error": "Days parameter must be positive"})

        history_data = await self.service.get_weather_history(city, days)
        if not history_data:
            return JSONResponse(status_code=404, content={"error": "City not found"})

        return JSONResponse(content=history_data)