import os
import secrets
from dotenv import load_dotenv

load_dotenv()

def _database_url():
    url = os.environ.get('DATABASE_URL') or 'sqlite:///marketplace.db'
    if url.startswith('postgres://'):
        url = 'postgresql://' + url[len('postgres://'):]
    if url.startswith('postgresql://') and '+psycopg' not in url:
        url = url.replace('postgresql://', 'postgresql+psycopg2://', 1)
    return url

class Config:
    # Never use a weak default in production — force env SECRET_KEY on Render
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)

    SQLALCHEMY_DATABASE_URI = _database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping': True}

    # ----- Session / cookie security -----
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    # Secure cookies only when not local
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production' or bool(os.environ.get('RENDER'))
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_SECURE = SESSION_COOKIE_SECURE
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 7  # 7 days

    # CSRF
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600 * 8  # 8 hours
    WTF_CSRF_SSL_STRICT = False  # Render terminates TLS at proxy

    # Behind Render / reverse proxy
    PREFERRED_URL_SCHEME = 'https'

    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')
    STRIPE_CONNECT_CLIENT_ID = os.environ.get('STRIPE_CONNECT_CLIENT_ID')
    PLATFORM_FEE_PERCENT = int(os.environ.get('PLATFORM_FEE_PERCENT', 10))
    APP_URL = os.environ.get('APP_URL', 'http://localhost:5000')

    MAX_CONTENT_LENGTH = 25 * 1024 * 1024
    UPLOAD_FOLDER = 'static/uploads'
    MAX_IMAGE_SIZE = 5 * 1024 * 1024
    MAX_IMAGES_PER_PRODUCT = 5
    ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp', 'gif'}

    LANGUAGES = ['fr', 'en', 'nl', 'de', 'fa']
    DEFAULT_LANGUAGE = 'fr'

    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'shapyaar@gmail.com')
    STRIPE_CONNECT_COUNTRY = os.environ.get('STRIPE_CONNECT_COUNTRY', 'BE')

    # Cloudinary (persistent images — survives Render redeploy)
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME', '')
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY', '')
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET', '')


    # Telegram notifications (BotFather token + admin chat/channel id)
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
    ADMIN_TELEGRAM_CHAT_ID = os.environ.get('ADMIN_TELEGRAM_CHAT_ID', '')


    # Rate limits (string format for Flask-Limiter)
    RATELIMIT_DEFAULT = '200 per hour'
    RATELIMIT_STORAGE_URI = 'memory://'
