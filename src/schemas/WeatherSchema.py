weather_response_schema = {
    "type": "object",
    "required": ["location", "timestamp", "data", "sources"],
    "properties": {
        "location": {
            "type": "object",
            "required": ["city", "lat", "lon"],
            "properties": {
                "city": {"type": "string"},
                "country": {"type": "string"},
                "lat": {"type": "number"},
                "lon": {"type": "number"}
            }
        },
        "timestamp": {
            "type": "string",
            "format": "date-time"
        },
        "data": {
            "type": "object",
            "required": ["temperature", "humidity", "description"],
            "properties": {
                "temperature": {
                    "type": "object",
                    "required": ["current", "unit"],
                    "properties": {
                        "current": {"type": "number"},
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                    }
                },
                "humidity": {"type": "number"},
                "description": {"type": "string"}
            }
        },
        "sources": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1
        }
    }
}
