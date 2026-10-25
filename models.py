from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=True)
    is_seller = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    stripe_account_id = db.Column(db.String(255), nullable=True)
    stripe_onboarding_complete = db.Column(db.Boolean, default=False)
    google_id = db.Column(db.String(255), nullable=True, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    products = db.relationship('Product', backref='seller', lazy='dynamic')
    orders = db.relationship('Order', backref='buyer', lazy='dynamic', foreign_keys='Order.buyer_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Integer, nullable=False)  # cents
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500), nullable=True)  # cover / first image (compat)
    is_active = db.Column(db.Boolean, default=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    images = db.relationship(
        'ProductImage',
        backref='product',
        lazy='joined',
        cascade='all, delete-orphan',
        order_by='ProductImage.sort_order'
    )

    def price_display(self):
        return f"{self.price / 100:.2f}"

    def cover_url(self):
        if self.images:
            return self.images[0].url
        return self.image_url

    def short_description(self, length=100):
        if not self.description:
            return ''
        if len(self.description) <= length:
            return self.description
        return self.description[:length].rsplit(' ', 1)[0] + '…'

    def __repr__(self):
        return f'<Product {self.name}>'


class ProductImage(db.Model):
    __tablename__ = 'product_images'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('cart_items', lazy='dynamic'))
    product = db.relationship('Product')


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)
    platform_fee = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default='pending')
    stripe_session_id = db.Column(db.String(255), nullable=True)
    stripe_payment_intent = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')

    def total_display(self):
        return f"{self.total_amount / 100:.2f}"


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    transfer_id = db.Column(db.String(255), nullable=True)

    product = db.relationship('Product')
    seller = db.relationship('User', foreign_keys=[seller_id])
