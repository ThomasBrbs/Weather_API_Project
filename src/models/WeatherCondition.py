from pydantic import BaseModel
from typing import Optional

class WeatherCondition(BaseModel):
    state: str
    description: Optional[str]
    humidity: Optional[float]
    pressure: Optional[float]
    visibility: Optional[float]