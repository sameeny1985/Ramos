import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, current_app, g
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import stripe
from authlib.integrations.flask_client import OAuth
from config import Config
from models import db, User, Product, CartItem, Order, OrderItem
from translations import get_translation, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE, TRANSLATIONS

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'

stripe.api_key = app.config.get('STRIPE_SECRET_KEY')

# Google OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config.get('GOOGLE_CLIENT_ID'),
    client_secret=app.config.get('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

# Ensure upload folder exists
os.makedirs(app.config.get('UPLOAD_FOLDER', 'static/uploads'), exist_ok=True)


def _(key, **kwargs):
    """Translate helper. Usage in templates: {{ _('home') }}"""
    lang = getattr(g, 'lang', DEFAULT_LANGUAGE)
    text = get_translation(key, lang)
    if kwargs:
        try:
            return text % kwargs
        except Exception:
            return text
    return text


@app.context_processor
def inject_i18n():
    """Make _ and language info available in all templates."""
    return {
        '_': _,
        'current_lang': getattr(g, 'lang', DEFAULT_LANGUAGE),
        'supported_languages': SUPPORTED_LANGUAGES,
        'is_rtl': getattr(g, 'lang', DEFAULT_LANGUAGE) == 'fa',
    }


@app.before_request
def set_language():
    """Determine language from session or Accept-Language, default French."""
    lang = session.get('lang')
    if not lang or lang not in SUPPORTED_LANGUAGES:
        # Try browser preference
        best = request.accept_languages.best_match(list(SUPPORTED_LANGUAGES.keys()))
        lang = best or DEFAULT_LANGUAGE
    g.lang = lang
    # Update login message according to language
    login_manager.login_message = _('please_login')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in SUPPORTED_LANGUAGES:
        session['lang'] = lang
    return redirect(request.referrer or url_for('index'))


@app.route('/become-seller', methods=['POST'])
@login_required
def become_seller():
    """Any logged-in user can become a seller."""
    if current_user.is_seller:
        flash('Vous êtes déjà vendeur.' if g.lang == 'fr' else 'You are already a seller.', 'info')
        return redirect(url_for('seller_dashboard'))
    current_user.is_seller = True
    db.session.commit()
    flash('Félicitations ! Vous êtes maintenant vendeur. Ajoutez votre premier produit.' if g.lang == 'fr' else 'Congratulations! You are now a seller. Add your first product.', 'success')
    return redirect(url_for('seller_dashboard'))




# ---------- Auth Routes ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        is_seller = request.form.get('is_seller') == 'on'

        if not username or not email or not password:
            flash(_('all_fields_required') if 'all_fields_required' in TRANSLATIONS else 'Tous les champs sont obligatoires.', 'danger')
            return redirect(url_for('register'))

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('Ce nom d\'utilisateur ou e-mail existe déjà.' if g.lang == 'fr' else 'Username or email already exists.', 'danger')
            return redirect(url_for('register'))

        user = User(username=username, email=email, is_seller=is_seller)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Inscription réussie ! Vous pouvez maintenant vous connecter.' if g.lang == 'fr' else 'Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            flash(f'Bienvenue {user.username} !' if g.lang == 'fr' else f'Welcome {user.username}!', 'success')
            return redirect(next_page or url_for('index'))
        flash('E-mail ou mot de passe incorrect.' if g.lang == 'fr' else 'Incorrect email or password.', 'danger')
    return render_template('login.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté.' if g.lang == 'fr' else 'You have been logged out.', 'info')
    return redirect(url_for('index'))


# ---------- Google OAuth ----------
@app.route('/login/google')
def google_login():
    """Redirect to Google account picker / consent screen."""
    if not app.config.get('GOOGLE_CLIENT_ID') or not app.config.get('GOOGLE_CLIENT_SECRET'):
        flash('Google login is not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET.' if g.lang != 'fr' else 'Connexion Google non configurée.', 'danger')
        return redirect(url_for('login'))
    redirect_uri = url_for('google_callback', _external=True)
    # prompt=select_account forces the Google account chooser
    return google.authorize_redirect(redirect_uri, prompt='select_account')


@app.route('/login/google/callback')
def google_callback():
    """Handle Google OAuth callback, create/login user."""
    try:
        token = google.authorize_access_token()
    except Exception as e:
        app.logger.error(f"Google OAuth error: {e}")
        flash('Erreur de connexion Google.' if g.lang == 'fr' else 'Google login failed.', 'danger')
        return redirect(url_for('login'))

    userinfo = token.get('userinfo')
    if not userinfo:
        # Fallback: fetch userinfo
        try:
            resp = google.get('https://openidconnect.googleapis.com/v1/userinfo')
            userinfo = resp.json()
        except Exception:
            flash('Impossible de récupérer les infos Google.' if g.lang == 'fr' else 'Could not get Google profile.', 'danger')
            return redirect(url_for('login'))

    email = (userinfo.get('email') or '').lower().strip()
    google_id = userinfo.get('sub')
    name = userinfo.get('name') or userinfo.get('given_name') or email.split('@')[0]

    if not email:
        flash('Email Google introuvable.' if g.lang == 'fr' else 'No email from Google.', 'danger')
        return redirect(url_for('login'))

    admin_email = (app.config.get('ADMIN_EMAIL') or 'shapyaar@gmail.com').lower()

    user = User.query.filter_by(email=email).first()
    if not user:
        # Create unique username
        base_username = name.replace(' ', '_').lower()[:40] or email.split('@')[0]
        username = base_username
        i = 1
        while User.query.filter_by(username=username).first():
            username = f"{base_username}{i}"
            i += 1

        user = User(
            username=username,
            email=email,
            google_id=google_id,
            is_admin=(email == admin_email),
            is_seller=False,
        )
        # No password for pure Google users
        db.session.add(user)
        db.session.commit()
    else:
        # Update google_id / admin flag if needed
        if google_id and not user.google_id:
            user.google_id = google_id
        if email == admin_email and not user.is_admin:
            user.is_admin = True
        db.session.commit()

    login_user(user, remember=True)
    flash(f'Bienvenue {user.username} !' if g.lang == 'fr' else f'Welcome {user.username}!', 'success')
    return redirect(url_for('index'))


# ---------- Main Pages ----------
@app.route('/')
def index():
    products = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).all()
    return render_template('index.html', products=products)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)


# ---------- Seller Dashboard ----------
@app.route('/seller/dashboard')
@login_required
def seller_dashboard():
    if not current_user.is_seller:
        flash('Vous n\'êtes pas vendeur.' if g.lang == 'fr' else 'You are not a seller.', 'warning')
        return redirect(url_for('index'))
    products = current_user.products.order_by(Product.created_at.desc()).all()
    sold_items = OrderItem.query.filter_by(seller_id=current_user.id).all()
    total_sales = sum(item.price * item.quantity for item in sold_items)
    return render_template('seller_dashboard.html', products=products, total_sales=total_sales)


@app.route('/seller/product/new', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_seller:
        flash('Seuls les vendeurs peuvent ajouter des produits.' if g.lang == 'fr' else 'Only sellers can add products.', 'warning')
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        price = request.form.get('price', '0')
        stock = request.form.get('stock', '0')
        try:
            price_cents = int(float(price) * 100)
            stock = int(stock)
        except ValueError:
            flash('Prix ou stock invalide.' if g.lang == 'fr' else 'Invalid price or stock.', 'danger')
            return redirect(url_for('add_product'))

        image_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                filename = f"{current_user.id}_{filename}"
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)
                image_url = url_for('static', filename=f'uploads/{filename}')

        product = Product(
            name=name,
            description=description,
            price=price_cents,
            stock=stock,
            image_url=image_url,
            seller_id=current_user.id
        )
        db.session.add(product)
        db.session.commit()
        flash('Produit ajouté avec succès.' if g.lang == 'fr' else 'Product added successfully.', 'success')
        return redirect(url_for('seller_dashboard'))
    return render_template('add_product.html')


@app.route('/seller/product/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.seller_id != current_user.id and not current_user.is_admin:
        flash('Accès refusé.' if g.lang == 'fr' else 'Access denied.', 'danger')
        return redirect(url_for('seller_dashboard'))
    if request.method == 'POST':
        product.name = request.form.get('name', '').strip()
        product.description = request.form.get('description', '').strip()
        try:
            product.price = int(float(request.form.get('price', '0')) * 100)
            product.stock = int(request.form.get('stock', '0'))
        except ValueError:
            flash('Prix ou stock invalide.' if g.lang == 'fr' else 'Invalid price or stock.', 'danger')
            return redirect(url_for('edit_product', product_id=product_id))
        product.is_active = request.form.get('is_active') == 'on'
        db.session.commit()
        flash('Produit mis à jour.' if g.lang == 'fr' else 'Product updated.', 'success')
        return redirect(url_for('seller_dashboard'))
    return render_template('edit_product.html', product=product)


@app.route('/seller/product/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.seller_id != current_user.id and not current_user.is_admin:
        flash('Accès refusé.' if g.lang == 'fr' else 'Access denied.', 'danger')
        return redirect(url_for('seller_dashboard'))
    product.is_active = False
    db.session.commit()
    flash('Produit désactivé.' if g.lang == 'fr' else 'Product deactivated.', 'info')
    return redirect(url_for('seller_dashboard'))


# ---------- Stripe Connect Onboarding for Sellers ----------
@app.route('/seller/connect-stripe')
@login_required
def connect_stripe():
    """Start Stripe Express onboarding. Bank details are entered only on Stripe."""
    if not current_user.is_seller:
        flash('Sellers only.', 'warning')
        return redirect(url_for('index'))

    secret = (app.config.get('STRIPE_SECRET_KEY') or '').strip()
    if not secret or not secret.startswith(('sk_test_', 'sk_live_')):
        flash('STRIPE_SECRET_KEY is missing or invalid in Environment variables.', 'danger')
        return redirect(url_for('seller_dashboard'))

    # Always set key in this request (in case gunicorn workers differ)
    stripe.api_key = secret

    try:
        if not current_user.stripe_account_id:
            country = (app.config.get('STRIPE_CONNECT_COUNTRY') or 'FR').strip().upper()
            # Prefer Express; if country fails, retry with US (best for Test mode)
            try:
                account = stripe.Account.create(
                    type='express',
                    country=country,
                    email=current_user.email,
                    capabilities={
                        'card_payments': {'requested': True},
                        'transfers': {'requested': True},
                    },
                    business_type='individual',
                    metadata={'user_id': str(current_user.id)},
                )
            except Exception as country_err:
                if country != 'US':
                    app.logger.warning(f"Connect country {country} failed ({country_err}), retry US")
                    account = stripe.Account.create(
                        type='express',
                        country='US',
                        email=current_user.email,
                        capabilities={
                            'card_payments': {'requested': True},
                            'transfers': {'requested': True},
                        },
                        business_type='individual',
                        metadata={'user_id': str(current_user.id)},
                    )
                else:
                    raise

            current_user.stripe_account_id = account.id
            db.session.commit()

        # Absolute URLs — must match the live domain (ramos-shop.onrender.com)
        base = (app.config.get('APP_URL') or request.url_root or '').rstrip('/')
        if not base.startswith('http'):
            base = request.url_root.rstrip('/')
        refresh_url = f"{base}/seller/connect-stripe"
        return_url = f"{base}/seller/dashboard?stripe=success"

        account_link = stripe.AccountLink.create(
            account=current_user.stripe_account_id,
            refresh_url=refresh_url,
            return_url=return_url,
            type='account_onboarding',
        )
        return redirect(account_link.url)

    except Exception as e:
        # Never 500 — always show message on dashboard
        app.logger.exception("Stripe Connect failed")
        err = str(e)
        # Clear broken account id so user can retry
        if current_user.stripe_account_id and ('No such account' in err or 'account' in err.lower() and 'invalid' in err.lower()):
            current_user.stripe_account_id = None
            current_user.stripe_onboarding_complete = False
            db.session.commit()
        flash(f'Stripe Connect error: {err}', 'danger')
        return redirect(url_for('seller_dashboard'))


@app.route('/seller/stripe-status')
@login_required
def stripe_status():
    if not current_user.stripe_account_id:
        return jsonify({'complete': False})
    account = stripe.Account.retrieve(current_user.stripe_account_id)
    complete = account.charges_enabled and account.payouts_enabled
    if complete and not current_user.stripe_onboarding_complete:
        current_user.stripe_onboarding_complete = True
        db.session.commit()
    return jsonify({
        'complete': complete,
        'charges_enabled': account.charges_enabled,
        'payouts_enabled': account.payouts_enabled
    })


# ---------- Cart ----------
@app.route('/cart')
@login_required
def cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in items if item.product.is_active)
    return render_template('cart.html', items=items, total=total)


@app.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    if not product.is_active or product.stock < 1:
        flash('Produit non disponible.' if g.lang == 'fr' else 'Product not available.', 'warning')
        return redirect(url_for('product_detail', product_id=product_id))

    item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if item:
        item.quantity += 1
    else:
        item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(item)
    db.session.commit()
    flash(f'{product.name} ajouté au panier.' if g.lang == 'fr' else f'{product.name} added to cart.', 'success')
    return redirect(url_for('cart'))


@app.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash('Accès refusé.' if g.lang == 'fr' else 'Access denied.', 'danger')
        return redirect(url_for('cart'))
    quantity = int(request.form.get('quantity', 1))
    if quantity <= 0:
        db.session.delete(item)
    else:
        item.quantity = min(quantity, item.product.stock)
    db.session.commit()
    return redirect(url_for('cart'))


@app.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash('Accès refusé.' if g.lang == 'fr' else 'Access denied.', 'danger')
        return redirect(url_for('cart'))
    db.session.delete(item)
    db.session.commit()
    flash('Article supprimé.' if g.lang == 'fr' else 'Item removed.', 'info')
    return redirect(url_for('cart'))


# ---------- Checkout with Stripe ----------
@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not items:
        flash('Votre panier est vide.' if g.lang == 'fr' else 'Your cart is empty.', 'warning')
        return redirect(url_for('cart'))

    line_items = []
    total = 0
    order_items_data = []

    for item in items:
        if not item.product.is_active or item.product.stock < item.quantity:
            flash(f'Stock insuffisant pour {item.product.name}.' if g.lang == 'fr' else f'Insufficient stock for {item.product.name}.', 'danger')
            return redirect(url_for('cart'))
        line_items.append({
            'price_data': {
                'currency': 'eur',  # Euro for French market
                'product_data': {
                    'name': item.product.name,
                    'description': f'{_("seller")}: {item.product.seller.username}',
                },
                'unit_amount': item.product.price,
            },
            'quantity': item.quantity,
        })
        total += item.product.price * item.quantity
        order_items_data.append({
            'product_id': item.product.id,
            'seller_id': item.product.seller_id,
            'quantity': item.quantity,
            'price': item.product.price,
        })

    platform_fee = int(total * app.config['PLATFORM_FEE_PERCENT'] / 100)

    order = Order(
        buyer_id=current_user.id,
        total_amount=total,
        platform_fee=platform_fee,
        status='pending'
    )
    db.session.add(order)
    db.session.flush()

    for data in order_items_data:
        oi = OrderItem(
            order_id=order.id,
            product_id=data['product_id'],
            seller_id=data['seller_id'],
            quantity=data['quantity'],
            price=data['price']
        )
        db.session.add(oi)

    db.session.commit()

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=url_for('checkout_success', order_id=order.id, _external=True) + '&session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('cart', _external=True),
            metadata={
                'order_id': order.id,
                'buyer_id': current_user.id,
            },
            customer_email=current_user.email,
            locale=g.lang if g.lang in ['fr', 'en', 'nl', 'de'] else 'fr',
        )
        order.stripe_session_id = checkout_session.id
        db.session.commit()
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        flash(f'Erreur de paiement : {str(e)}' if g.lang == 'fr' else f'Payment error: {str(e)}', 'danger')
        return redirect(url_for('cart'))


@app.route('/checkout/success')
@login_required
def checkout_success():
    order_id = request.args.get('order_id')
    session_id = request.args.get('session_id')
    order = Order.query.get_or_404(order_id)
    if order.buyer_id != current_user.id:
        flash('Accès refusé.' if g.lang == 'fr' else 'Access denied.', 'danger')
        return redirect(url_for('index'))

    if session_id:
        try:
            sess = stripe.checkout.Session.retrieve(session_id)
            if sess.payment_status == 'paid':
                order.status = 'paid'
                order.stripe_payment_intent = sess.payment_intent
                for item in order.items:
                    product = item.product
                    product.stock = max(0, product.stock - item.quantity)
                CartItem.query.filter_by(user_id=current_user.id).delete()
                db.session.commit()
                _transfer_to_sellers(order)
        except Exception as e:
            app.logger.error(f"Stripe verify error: {e}")

    return render_template('checkout_success.html', order=order)


def _transfer_to_sellers(order):
    from collections import defaultdict
    seller_totals = defaultdict(int)
    for item in order.items:
        seller_totals[item.seller_id] += item.price * item.quantity

    for seller_id, amount in seller_totals.items():
        seller = User.query.get(seller_id)
        if not seller or not seller.stripe_account_id or not seller.stripe_onboarding_complete:
            continue
        seller_share = int(amount * (100 - app.config['PLATFORM_FEE_PERCENT']) / 100)
        if seller_share <= 0:
            continue
        try:
            transfer = stripe.Transfer.create(
                amount=seller_share,
                currency='eur',
                destination=seller.stripe_account_id,
                transfer_group=f'order_{order.id}',
                metadata={'order_id': order.id, 'seller_id': seller_id}
            )
            for item in order.items:
                if item.seller_id == seller_id and not item.transfer_id:
                    item.transfer_id = transfer.id
                    break
            db.session.commit()
        except Exception as e:
            app.logger.error(f"Transfer failed for seller {seller_id}: {e}")


@app.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = app.config.get('STRIPE_WEBHOOK_SECRET')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError:
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError:
        return jsonify({'error': 'Invalid signature'}), 400

    if event['type'] == 'checkout.session.completed':
        session_obj = event['data']['object']
        order_id = session_obj.get('metadata', {}).get('order_id')
        if order_id:
            order = Order.query.get(int(order_id))
            if order and order.status != 'paid':
                order.status = 'paid'
                order.stripe_payment_intent = session_obj.get('payment_intent')
                for item in order.items:
                    product = item.product
                    product.stock = max(0, product.stock - item.quantity)
                db.session.commit()
                _transfer_to_sellers(order)

    return jsonify({'status': 'success'}), 200


@app.route('/orders')
@login_required
def my_orders():
    orders = Order.query.filter_by(buyer_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=orders)


@app.route('/seller/orders')
@login_required
def seller_orders():
    if not current_user.is_seller:
        flash('Réservé aux vendeurs.' if g.lang == 'fr' else 'Sellers only.', 'warning')
        return redirect(url_for('index'))
    items = OrderItem.query.filter_by(seller_id=current_user.id).order_by(OrderItem.id.desc()).all()
    return render_template('seller_orders.html', items=items)


@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Accès administrateur requis.' if g.lang == 'fr' else 'Admin access required.', 'danger')
        return redirect(url_for('index'))
    users = User.query.order_by(User.created_at.desc()).all()
    products = Product.query.order_by(Product.created_at.desc()).all()
    orders = Order.query.order_by(Order.created_at.desc()).limit(100).all()
    total_revenue = sum(o.total_amount for o in Order.query.filter_by(status='paid').all())
    total_fees = sum(o.platform_fee for o in Order.query.filter_by(status='paid').all())
    stats = {
        'users': User.query.count(),
        'sellers': User.query.filter_by(is_seller=True).count(),
        'products': Product.query.filter_by(is_active=True).count(),
        'orders': Order.query.count(),
        'paid_orders': Order.query.filter_by(status='paid').count(),
        'revenue': total_revenue,
        'fees': total_fees,
    }
    return render_template('admin.html', users=users, products=products, orders=orders, stats=stats)


@app.route('/admin/user/<int:user_id>/toggle-admin', methods=['POST'])
@login_required
def admin_toggle_admin(user_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Vous ne pouvez pas modifier votre propre statut admin.' if g.lang == 'fr' else 'Cannot change your own admin status.', 'warning')
        return redirect(url_for('admin'))
    user.is_admin = not user.is_admin
    db.session.commit()
    flash('Statut admin mis à jour.' if g.lang == 'fr' else 'Admin status updated.', 'success')
    return redirect(url_for('admin'))


@app.route('/admin/user/<int:user_id>/toggle-seller', methods=['POST'])
@login_required
def admin_toggle_seller(user_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))
    user = User.query.get_or_404(user_id)
    user.is_seller = not user.is_seller
    db.session.commit()
    flash('Statut vendeur mis à jour.' if g.lang == 'fr' else 'Seller status updated.', 'success')
    return redirect(url_for('admin'))


@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Vous ne pouvez pas vous supprimer.' if g.lang == 'fr' else 'Cannot delete yourself.', 'warning')
        return redirect(url_for('admin'))
    # Soft approach: deactivate products, delete cart, keep orders for history
    Product.query.filter_by(seller_id=user.id).update({'is_active': False})
    CartItem.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    flash('Utilisateur supprimé.' if g.lang == 'fr' else 'User deleted.', 'info')
    return redirect(url_for('admin'))


@app.route('/admin/product/<int:product_id>/toggle', methods=['POST'])
@login_required
def admin_toggle_product(product_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))
    product = Product.query.get_or_404(product_id)
    product.is_active = not product.is_active
    db.session.commit()
    flash('Produit mis à jour.' if g.lang == 'fr' else 'Product updated.', 'success')
    return redirect(url_for('admin'))


@app.route('/admin/product/<int:product_id>/delete', methods=['POST'])
@login_required
def admin_delete_product(product_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))
    product = Product.query.get_or_404(product_id)
    product.is_active = False
    db.session.commit()
    flash('Produit désactivé.' if g.lang == 'fr' else 'Product deactivated.', 'info')
    return redirect(url_for('admin'))


@app.route('/admin/product/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_product(product_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form.get('name', '').strip()
        product.description = request.form.get('description', '').strip()
        try:
            product.price = int(float(request.form.get('price', '0')) * 100)
            product.stock = int(request.form.get('stock', '0'))
        except ValueError:
            flash('Prix/stock invalide.' if g.lang == 'fr' else 'Invalid price/stock.', 'danger')
            return redirect(url_for('admin_edit_product', product_id=product_id))
        product.is_active = request.form.get('is_active') == 'on'
        db.session.commit()
        flash('Produit mis à jour.' if g.lang == 'fr' else 'Product updated.', 'success')
        return redirect(url_for('admin'))
    return render_template('edit_product.html', product=product, admin_mode=True)


# ---------- Create tables & seed ----------
def create_tables():
    with app.app_context():
        db.create_all()
        admin_email = app.config.get('ADMIN_EMAIL', 'shapyaar@gmail.com').lower()
        admin = User.query.filter_by(email=admin_email).first()
        if not admin:
            admin = User(
                username='admin',
                email=admin_email,
                is_admin=True,
                is_seller=True,
            )
            # Random password (login should be via Google)
            admin.set_password(secrets.token_urlsafe(32))
            db.session.add(admin)
            db.session.commit()
            print(f"Admin created: {admin_email} (use Google login)")
        elif not admin.is_admin:
            admin.is_admin = True
            db.session.commit()
            print(f"Admin flag set for: {admin_email}")

try:
    create_tables()
except Exception as e:
    print(f"DB init note: {e}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
