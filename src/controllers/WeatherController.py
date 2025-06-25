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
        print(weather_data)
        if not weather_data:
            return JSONResponse(status_code=404, content={"error": "City not found"})

        return JSONResponse(content=weather_data)
