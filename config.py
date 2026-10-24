import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///marketplace.db'
    if SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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

    # Google OAuth
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

    # Admin email (Google login with this email becomes admin)
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'shapyaar@gmail.com')
    STRIPE_CONNECT_COUNTRY = os.environ.get('STRIPE_CONNECT_COUNTRY', 'FR')
