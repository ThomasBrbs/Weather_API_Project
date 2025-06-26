**Weather API**

Cette API est une application FastAPI organisée autour d’un service météo, avec une architecture claire en couches (controllers, services, models).
Elle expose plusieurs routes pour récupérer la météo actuelle, les prévisions, et l’historique, le tout via des requêtes POST structurées.



**Fonctionnalités principales**
-Météo actuelle (/weather/current)

-Prévisions météo (/weather/forecast)

-Historique météo (/weather/history)

-Health check (/health)

 **Structure du projet**
Le projet respecte une architecture modulaire inspirée du modèle MVC :

<pre>project/
│
├── api.py                      
├── src/
│   ├── controllers/
│   │   └── WeatherController.py 
│   ├── models/
│   │   └── ModelRequest.py      
│   └── services/
│       └── WeatherService.py    </pre>

api.py : Déclare les routes et connecte les différentes couches
.

controllers/ : Gère la logique métier (ex : appel des services, validation).

services/ : Encapsule l’accès aux données ou aux API externes.

models/ : Définit les schémas de données attendus en entrée.




**Endpoints (Routes)**
POST /weather/current
Description : Retourne la météo actuelle pour la localisation fournie.

Body (JSON):
Doit respecter le schéma ModelRequest.

Réponse : Détail de la météo du moment.

POST /weather/forecast
Description : Retourne les prévisions météo pour la localisation et la période fournies.

Body (JSON):
Doit respecter le schéma ModelRequest.

Réponse : Prévisions météorologiques.

POST /weather/history
Description : Retourne l’historique météo sur une période définie.

Body (JSON):
Doit respecter le schéma ModelRequest.

Réponse : Données météo historiques.

GET /health
Description : Permet de vérifier que l’API est opérationnelle.

Réponse : {"status": "ok"}




**Lancement du projet**
Installer les dépendances

<pre>pip install -r requirements.txt</pre>

Lancer le serveur


uvicorn api:app --reload
Tester dans un navigateur ou via Swagger UI




**Exemple de requête POST**
json
<pre>POST /weather/current
{
  "city": "Paris",
  "country": "France"
}
</pre>



**Points clés**
Toutes les routes météo attendent un JSON conforme au modèle ModelRequest.

La logique est centralisée dans le WeatherController qui délègue au WeatherService.

L’API est conçue pour être extensible et maintenable.

N’hésite pas à compléter la section sur le schéma d’entrée (ModelRequest) avec ses champs exacts, si besoin !





uvicorn api:app --reload
Run in the port : http://127.0.0.1:8000
