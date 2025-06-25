import requests
from jsonschema import validate

from schemas.WeatherSchema import weather_response_schema
BASE_URL = "http://127.0.0.1:8000"

def test_get_current_weather_valid_city():
    payload = {"city": "Paris"}
    response = requests.post(f"{BASE_URL}/weather/current", json=payload)
    assert response.status_code == 200

    data = response.json()
    validate(instance=data, schema=weather_response_schema)

    assert data["location"]["city"].lower() == "paris"
    assert isinstance(data["data"]["temperature"]["current"], (int, float))