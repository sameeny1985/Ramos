import os
from dotenv import load_dotenv

load_dotenv()

def _database_url():
    url = os.environ.get('DATABASE_URL') or 'sqlite:///marketplace.db'
    # Render sometimes gives postgres:// — SQLAlchemy needs postgresql://
    if url.startswith('postgres://'):
        url = 'postgresql://' + url[len('postgres://'):]
    # Force psycopg2 driver so we don't need the separate "psycopg" (v3) package path
    if url.startswith('postgresql://') and '+psycopg' not in url:
        url = url.replace('postgresql://', 'postgresql+psycopg2://', 1)
    return url

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = _database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Avoid SSL issues on some Render Postgres plans
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
    }

    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')
    STRIPE_CONNECT_CLIENT_ID = os.environ.get('STRIPE_CONNECT_CLIENT_ID')
    PLATFORM_FEE_PERCENT = int(os.environ.get('PLATFORM_FEE_PERCENT', 10))
    APP_URL = os.environ.get('APP_URL', 'http://localhost:5000')

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = 'static/uploads'

    LANGUAGES = ['fr', 'en', 'nl', 'de', 'fa']
    DEFAULT_LANGUAGE = 'fr'

    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'shapyaar@gmail.com')
    STRIPE_CONNECT_COUNTRY = os.environ.get('STRIPE_CONNECT_COUNTRY', 'BE').strip().upper()
