from pydantic import BaseModel
from typing import Optional

class Wind(BaseModel):
    speed: float
    direction: Optional[str]
    unit: str = "km/h"