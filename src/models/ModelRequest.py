from pydantic import BaseModel

class ModelRequest(BaseModel):
    city: str