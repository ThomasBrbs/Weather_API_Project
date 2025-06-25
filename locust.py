from locust import HttpUser, task, between
import random
from locust import events
import logging

class WeatherAPIUser(HttpUser):
    wait_time = between(1, 3)

    cities = ["Paris", "London", "Tokyo", "New York"]

    @task(3)
    def get_current_weather(self):
        city = random.choice(self.cities)
        with self.client.post("/weather/current", json={"city": city}, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")

    @task(2)
    def get_weather_forecast(self):
        city = random.choice(self.cities)
        with self.client.post("/weather/forecast", json={"city": city}, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")

    @task(1)
    def get_weather_history(self):
        city = random.choice(self.cities)
        with self.client.post("/weather/history", json={"city": city, "days": 7}, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")

    @task(1)
    def health_check(self):
        self.client.get("/health")

    @events.test_start.add_listener
    def on_test_start(environment, **kwargs):
        logging.info("Test de charge démarré")

    @events.test_stop.add_listener
    def on_test_stop(environment, **kwargs):
        logging.info("Test de charge terminé")
        
        stats = environment.stats
        if stats.total.avg_response_time > 2000:
            logging.error("ÉCHEC: Temps de réponse trop élevé")
        if stats.total.num_failures / stats.total.num_requests > 0.05:
            logging.error("ÉCHEC: Taux d'erreur trop élevé")
