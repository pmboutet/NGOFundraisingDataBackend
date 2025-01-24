# NGO Fundraising Data Generator

Django REST API for generating synthetic fundraising data based on YAML configurations.

## Local Installation

```bash
# Clone repo
git clone https://github.com/pmboutet/NGOFundraisingDataBackend.git
cd NGOFundraisingDataBackend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

API available at `http://localhost:8000`

## Environment Configuration

### Development (default)
- Debug enabled
- SQLite database
- Console emails
- Configuration in `config/settings/development.py`

### Production
Set environment variables:
```bash
export DJANGO_SETTINGS_MODULE=config.settings.production
export DJANGO_SECRET_KEY=your-secret-key
export DATABASE_URL=postgresql://...
export EMAIL_HOST=smtp.example.com
export EMAIL_HOST_USER=user@example.com
export EMAIL_HOST_PASSWORD=password
```

## API Endpoints

- `/api/generate/` - POST - Generate dataset from YAML config
- `/api/docs/` - GET - Swagger API documentation

## Basic Usage

1. Generate dataset using a YAML config:
```python
import requests

config = """
config:
  donors: 100
  timeframe:
    start: 2023-01-01
    end: 2023-12-31
  donation_types:
    - name: one_time
      weight: 70
      amount_range: [10, 1000]
    - name: monthly
      weight: 30
      amount_range: [5, 100]
"""

response = requests.post(
    'http://localhost:8000/api/generate/',
    json={'config': config}
)

data = response.json()
print(data)
```

## Tests

```bash
python manage.py test
```

## Heroku Deployment

```bash
# Create app
heroku create

# Configure environment
heroku config:set DJANGO_SETTINGS_MODULE=config.settings.production
heroku config:set DJANGO_SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
```