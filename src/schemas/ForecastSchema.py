forecast_response_schema = {
    "type": "object",
    "required": ["location", "timestamp", "forecast", "sources"],
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
        "forecast": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["date", "temperature", "humidity", "description"],
                "properties": {
                    "date": {"type": "string", "format": "date"},
                    "temperature": {
                        "type": "object",
                        "required": ["min", "max", "unit"],
                        "properties": {
                            "min": {"type": "number"},
                            "max": {"type": "number"},
                            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                        }
                    },
                    "humidity": {"type": "number"},
                    "description": {"type": "string"}
                }
            }
        },
        "sources": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1
        }
    }
}
