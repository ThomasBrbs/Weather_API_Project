from pydantic import BaseModel
from typing import Optional, Dict

class Location(BaseModel):
    city: str
    country: Optional[str]
    coordinates: Optional[Dict[str, float]] 