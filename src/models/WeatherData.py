from pydantic import BaseModel
from datetime import datetime
from Temperature import Temperature
from WeatherCondition import WeatherCondition
from Wind import Wind

class WeatherData(BaseModel):
    timestamp: datetime
    temperature: Temperature
    condition: WeatherCondition
    wind: Wind
