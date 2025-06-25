import httpx
from decouple import Config, RepositoryEnv
import asyncio
from datetime import datetime, timedelta

DOTENV_FILE = "./config/.env"


class WeatherService:
    def __init__(self):
        env_config = Config(RepositoryEnv(DOTENV_FILE))
        self.openweather_key = env_config.get("OPENWEATHER_API_KEY")
        self.weatherapi_key = env_config.get("WEATHERAPI_KEY")
        self.api_key_weather = env_config.get("OPENWEATHER_API_KEY")
        self.open_meteo_base = "https://api.open-meteo.com/v1"
        self.base_url = "http://api.weatherapi.com/v1"

    async def get_current_weather(self, city: str):
        try:
            # Appels parallèles aux différentes sources
            async with httpx.AsyncClient() as client:
                results = await self._gather_weather_data(client, city)

            return self._aggregate_weather_data(results, city)

        except Exception as e:
            raise Exception(f"Failed to fetch weather for {city}: {str(e)}")

    async def _gather_weather_data(self, client, city):
        tasks = [
            self._get_openweather_data(client, city),
            self._get_weatherapi_data(client, city),
            self._get_openmeteo_data(client, city)
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if not isinstance(r, Exception) and r]

    async def _get_openweather_data(self, client, city):
        if not self.openweather_key:
            return None

        try:
            url = "https://api.openweathermap.org/data/2.5/weather"
            resp = await client.get(url, params={
                "q": city,
                "appid": self.openweather_key,
                "units": "metric"
            })

            data = resp.json()
            return {
                "source": "openweather",
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"]
            }
        except Exception:
            return None

    async def _get_weatherapi_data(self, client, city):
        if not self.weatherapi_key:
            return None

        try:
            url = f"http://api.weatherapi.com/v1/current.json"
            resp = await client.get(url, params={
                "key": self.weatherapi_key,
                "q": city,
                "aqi": "no"
            })

            data = resp.json()
            return {
                "source": "weatherapi",
                "temperature": data["current"]["temp_c"],
                "humidity": data["current"]["humidity"],
                "description": data["current"]["condition"]["text"]
            }
        except Exception:
            return None

    async def _get_openmeteo_data(self, client, city):
        coords = self._get_city_coordinates(city)
        if not coords:
            return None

        try:
            url = f"{self.open_meteo_base}/forecast"
            resp = await client.get(url, params={
                "latitude": coords["lat"],
                "longitude": coords["lon"],
                "current_weather": True,
                "hourly": "temperature_2m,relativehumidity_2m"
            })

            data = resp.json()
            return {
                "source": "open-meteo",
                "temperature": data["current_weather"]["temperature"],
                "humidity": data["hourly"]["relativehumidity_2m"][0],
                "description": self._get_weather_description(data["current_weather"]["weathercode"])
            }
        except Exception:
            return None

    def _get_city_coordinates(self, city: str):
        cities = {
            "paris": {"lat": 48.8566, "lon": 2.3522, "country": "France"},
            "london": {"lat": 51.5074, "lon": -0.1278, "country": "UK"},
            "tokyo": {"lat": 35.6762, "lon": 139.6503, "country": "Japan"},
            "new york": {"lat": 40.7128, "lon": -74.0060, "country": "USA"}
        }
        return cities.get(city.lower())


    def _get_weather_description(self, code: int) -> str:
        mapping = {
            0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Depositing rime fog", 51: "Light drizzle",
            61: "Light rain", 71: "Light snow", 80: "Rain showers"
            # Add more codes as needed
        }
        return mapping.get(code, "Unknown")

    def _aggregate_weather_data(self, sources, city):
        if not sources:
            raise Exception("No weather data available")

        avg_temp = sum(s["temperature"] for s in sources) / len(sources)
        avg_humidity = sum(s["humidity"] for s in sources) / len(sources)
        description = sources[0]["description"]  

        coords = self._get_city_coordinates(city)
        if not coords:
            coords = {"lat": 0, "lon": 0}
        location_data = coords or {"lat": 0, "lon": 0, "country": ""}
        
        return {
            "location": {
                "city": city,
                "lat": coords["lat"],
                "lon": coords["lon"],
                "country": location_data.get("country", "")
            },
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "data": {
                "temperature": {
                    "current": round(avg_temp, 1),
                    "unit": "celsius"
                },
                "humidity": round(avg_humidity),
                "description": description
            },
            "sources": [s["source"] for s in sources]
        }
        
    async def get_weather_forecast(self, city: str):
        coords = self._get_city_coordinates(city)
        if not coords:
            raise Exception("City not found")

        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/forecast.json"
                resp = await client.get(url, params={
                    "key": self.weatherapi_key,
                    "q": city,
                    "days": 3,
                    "aqi": "no",
                    "alerts": "no"
                })
                data = resp.json()

            forecast_days = data.get("forecast", {}).get("forecastday", [])
            if not forecast_days:
                raise Exception("No forecast data found")

            # Format simplifié de la réponse
            return {
                "location": {
                    "city": city,
                    "lat": coords["lat"],
                    "lon": coords["lon"],
                    "country": coords.get("country", "")
                },
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "forecast": [
                    {
                        "date": day["date"],
                        "description": day["day"]["condition"]["text"],
                        "temperature": {
                            "min": day["day"]["mintemp_c"],
                            "max": day["day"]["maxtemp_c"],
                            "unit": "celsius"
                        },
                        "humidity": day["day"]["avghumidity"]
                    }
                    for day in forecast_days
                ],
                "sources": ["weatherapi"]
            }
        except Exception as e:
            raise Exception(f"Failed to fetch forecast for {city}: {str(e)}")

    async def get_weather_history(self, city: str, days: int = 7):
        coords = self._get_city_coordinates(city)
        if not coords:
            raise Exception("City not found")

        history = []
        async with httpx.AsyncClient() as client:
            end_date = datetime.utcnow()
            for i in range(days):
                date = (end_date - timedelta(days=i)).strftime("%Y-%m-%d")
                url = f"{self.base_url}/history.json"
                resp = await client.get(url, params={
                    "key": self.weatherapi_key,
                    "q": city,
                    "dt": date,
                    "aqi": "no",
                    "alerts": "no"
                })
                data = resp.json()
                day_data = data.get("forecast", {}).get("forecastday", [])
                if day_data:
                    day = day_data[0]
                    history.append({
                        "date": day["date"],
                        "description": day["day"]["condition"]["text"],
                        "temperature": {
                            "min": day["day"]["mintemp_c"],
                            "max": day["day"]["maxtemp_c"],
                            "unit": "celsius"
                        },
                        "humidity": day["day"]["avghumidity"]
                    })

        if not history:
            raise Exception("No history data found")

        return {
            "location": {
                "city": city,
                "lat": coords["lat"],
                "lon": coords["lon"],
                "country": coords.get("country", "")
            },
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "history": history,
            "sources": ["weatherapi"]
        }


