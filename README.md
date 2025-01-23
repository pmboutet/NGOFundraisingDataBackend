# NGO Fundraising Data Generator

API REST Django pour générer des données de collecte de fonds synthétiques basées sur des configurations YAML.

## Installation locale

1. Cloner le repo
```bash
git clone https://github.com/pmboutet/NGOFundraisingDataBackend.git
cd NGOFundraisingDataBackend
```

2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Lancer les migrations
```bash
python manage.py migrate
```

5. Démarrer le serveur
```bash
python manage.py runserver
```

L'API sera disponible sur `http://localhost:8000`

## Endpoints API

- `/api/generate/` - POST - Génère un dataset basé sur la configuration YAML

## Documentation API

La documentation Swagger est disponible sur `/api/docs/`

## Déploiement

L'application est configurée pour Heroku. Pour le déploiement:

1. Créer une application Heroku
2. Configurer les variables d'environnement
3. Déployer via Git

## Tests

Pour lancer les tests:
```bash
python manage.py test
```