from pydantic import BaseModel
from typing import Optional

class Temperature(BaseModel):
    current: float
    feels_like: Optional[float]
    min: Optional[float]
    max: Optional[float]
    unit: str = "celsius"