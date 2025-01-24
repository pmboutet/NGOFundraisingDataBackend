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

## Configuration des environnements

### Développement (par défaut)
- Debug activé
- Base de données SQLite
- Emails en console
- Configuration dans `config/settings/development.py`

### Production
Définir les variables d'environnement suivantes:
```bash
export DJANGO_SETTINGS_MODULE=config.settings.production
export DJANGO_SECRET_KEY=your-secret-key
export DATABASE_URL=postgresql://...
export EMAIL_HOST=smtp.example.com
export EMAIL_HOST_USER=user@example.com
export EMAIL_HOST_PASSWORD=password
```

## Endpoints API

- `/api/generate/` - POST - Génère un dataset basé sur la configuration YAML
- `/api/docs/` - GET - Documentation Swagger de l'API

## Tests

Pour lancer les tests:
```bash
python manage.py test
```

## Déploiement Heroku

1. Créer une application Heroku
```bash
heroku create
```

2. Configurer les variables d'environnement
```bash
heroku config:set DJANGO_SETTINGS_MODULE=config.settings.production
heroku config:set DJANGO_SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
```

3. Déployer
```bash
git push heroku main
```

4. Lancer les migrations
```bash
heroku run python manage.py migrate
```