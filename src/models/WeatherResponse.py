from pydantic import BaseModel
from typing import Optional, Union, List

from Location import Location
from WeatherData import WeatherData
from Wind import Wind

class WeatherResponse(BaseModel):
    location: Location
    data: Union[WeatherData, List[WeatherData]]
    sources: List[str]
    message: Optional[str] = None