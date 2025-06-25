class LoadTestConfig:
    # URLs de test
    BASE_URL = "http://127.0.0.1:8000"
    
    # Profils de charge
    LIGHT_LOAD = {
        "users": 10,
        "spawn_rate": 2,
        "duration": "2m"
    }
    
    NORMAL_LOAD = {
        "users": 50,
        "spawn_rate": 5,
        "duration": "10m"
    }
    
    STRESS_LOAD = {
        "users": 200,
        "spawn_rate": 10,
        "duration": "15m"
    }
    
    # Villes pour les tests
    CITIES = [
        "Paris", "London", "Berlin", "Madrid", "Rome",
        "Tokyo", "Sydney", "New York", "Los Angeles"
    ]