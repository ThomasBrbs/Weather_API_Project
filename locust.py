from locust import HttpUser, task, between
import random
from locust import events
import logging

class WeatherAPIUser(HttpUser):
    # Temps d'attente entre les requêtes (1 à 3 secondes)
    wait_time = between(1, 3)
    
    def on_start(self):
        """Exécuté au démarrage de chaque utilisateur"""
        # Initialisation si nécessaire (login, setup, etc.)
        pass
    
    @task(3)  # Poids 3 : cette tâche sera exécutée 3x plus souvent
    def get_current_weather(self):
        """Test de l'endpoint météo actuelle"""
        cities = ["Paris", "London", "Tokyo", "New York", "Berlin"]
        city = random.choice(cities)
        
        with self.client.post(f"/weather/current/{city}", 
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(2)  # Poids 2
    def get_weather_forecast(self):
        """Test de l'endpoint prévisions"""
        cities = ["Paris", "Madrid", "Rome"]
        city = random.choice(cities)
        
        self.client.post(f"/weather/forecast/{city}")
    
    @task(1)  # Poids 1 : moins fréquent
    def get_weather_history(self):
        """Test de l'endpoint historique"""
        self.client.post("/weather/history/Paris?days=7")
    
    @task(1)
    def health_check(self):
        """Vérification de santé de l'API"""
        self.client.get("/health")
        
        
        
    @events.test_start.add_listener
    def on_test_start(environment, **kwargs):
        logging.info("Test de charge démarré")

    @events.test_stop.add_listener
    def on_test_stop(environment, **kwargs):
        logging.info("Test de charge terminé")
        
        # Génération de rapport personnalisé
        stats = environment.stats
        
        # Critères de succès/échec
        if stats.total.avg_response_time > 2000:  # > 2 secondes
            logging.error("ÉCHEC: Temps de réponse trop élevé")
        
        if stats.total.num_failures / stats.total.num_requests > 0.05:  # > 5% d'erreurs
            logging.error("ÉCHEC: Taux d'erreur trop élevé")