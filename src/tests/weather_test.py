import pytest
import requests
from jsonschema import validate

import pytest
from unittest.mock import AsyncMock, patch
from services.WeatherService import WeatherService

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
    


@pytest.mark.asyncio
async def test_aggregate_weather_data_from_multiple_sources():
    service = WeatherService()

    with patch.object(service, '_gather_weather_data', return_value=[
        # quand on utilise gather... on va retourner ces valeurs la, on pourra donc verifier ensuite si l'aggregation est juste ou non
        {"source": "openweather", "temperature": 20, "humidity": 65, "description": "Cloudy"},
        {"source": "weatherapi", "temperature": 22, "humidity": 70, "description": "Partly cloudy"},
    ]):
        result = await service.get_current_weather("Paris")

        assert isinstance(result, dict)
        assert "data" in result
        assert result["data"]["temperature"]["current"] == 21  # moyenne de 20 et 22
        assert set(result["sources"]) >= {"openweather", "weatherapi"}
        assert result["location"]["city"].lower() == "paris"


@pytest.mark.asyncio
async def test_fallback_when_one_source_fails():
    service = WeatherService()

    with patch.object(service, '_gather_weather_data', return_value=[
        {"source": "weatherapi", "temperature": 22, "humidity": 70, "description": "Clear"}
    ]):
        result = await service.get_current_weather("Paris")

        assert result["data"]["temperature"]["current"] == 22
        assert "weatherapi" in result["sources"]
        assert len(result["sources"]) == 1
