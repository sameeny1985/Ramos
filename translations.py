# Simple multi-language translation system (no external deps beyond Flask)
# Default language: French (fr)
# Supported: fr, en, nl, de, fa

TRANSLATIONS = {
    # ========== Site & Navigation ==========
    "site_name": {
        "fr": "Ramos",
        "en": "Ramos",
        "nl": "Ramos",
        "de": "Ramos",
        "fa": "Ramos"
    },
    "home": {
        "fr": "Accueil",
        "en": "Home",
        "nl": "Home",
        "de": "Startseite",
        "fa": "خانه"
    },
    "seller_panel": {
        "fr": "Espace vendeur",
        "en": "Seller Dashboard",
        "nl": "Verkoperspaneel",
        "de": "Verkäuferbereich",
        "fa": "پنل فروشنده"
    },
    "cart": {
        "fr": "Panier",
        "en": "Cart",
        "nl": "Winkelwagen",
        "de": "Warenkorb",
        "fa": "سبد خرید"
    },
    "my_orders": {
        "fr": "Mes commandes",
        "en": "My Orders",
        "nl": "Mijn bestellingen",
        "de": "Meine Bestellungen",
        "fa": "سفارش‌های من"
    },
    "login": {
        "fr": "Connexion",
        "en": "Login",
        "nl": "Inloggen",
        "de": "Anmelden",
        "fa": "ورود"
    },
    "register": {
        "fr": "Inscription",
        "en": "Register",
        "nl": "Registreren",
        "de": "Registrieren",
        "fa": "ثبت‌نام"
    },
    "logout": {
        "fr": "Déconnexion",
        "en": "Logout",
        "nl": "Uitloggen",
        "de": "Abmelden",
        "fa": "خروج"
    },
    "admin": {
        "fr": "Admin",
        "en": "Admin",
        "nl": "Admin",
        "de": "Admin",
        "fa": "ادمین"
    },

    # ========== Homepage ==========
    "welcome_title": {
        "fr": "Bienvenue sur Ramos",
        "en": "Welcome to Ramos",
        "nl": "Welkom bij Ramos",
        "de": "Willkommen bei Ramos",
        "fa": "به Ramos خوش آمدید"
    },
    "welcome_subtitle": {
        "fr": "Achetez et vendez facilement avec un paiement sécurisé Stripe",
        "en": "Buy and sell easily with secure Stripe payments",
        "nl": "Koop en verkoop eenvoudig met veilige Stripe-betalingen",
        "de": "Kaufen und verkaufen Sie einfach mit sicheren Stripe-Zahlungen",
        "fa": "خرید و فروش آسان با پرداخت امن Stripe"
    },
    "no_products": {
        "fr": "Aucun produit pour le moment.",
        "en": "No products yet.",
        "nl": "Nog geen producten.",
        "de": "Noch keine Produkte.",
        "fa": "هنوز محصولی ثبت نشده است."
    },
    "add_first_product": {
        "fr": "Ajoutez votre premier produit",
        "en": "Add your first product",
        "nl": "Voeg je eerste product toe",
        "de": "Fügen Sie Ihr erstes Produkt hinzu",
        "fa": "اولین محصول را اضافه کنید"
    },
    "view": {
        "fr": "Voir",
        "en": "View",
        "nl": "Bekijken",
        "de": "Ansehen",
        "fa": "مشاهده"
    },
    "seller": {
        "fr": "Vendeur",
        "en": "Seller",
        "nl": "Verkoper",
        "de": "Verkäufer",
        "fa": "فروشنده"
    },

    # ========== Product ==========
    "stock": {
        "fr": "Stock",
        "en": "Stock",
        "nl": "Voorraad",
        "de": "Lagerbestand",
        "fa": "موجودی"
    },
    "out_of_stock": {
        "fr": "Rupture de stock",
        "en": "Out of stock",
        "nl": "Niet op voorraad",
        "de": "Nicht vorrätig",
        "fa": "ناموجود"
    },
    "add_to_cart": {
        "fr": "Ajouter au panier",
        "en": "Add to cart",
        "nl": "Toevoegen aan winkelwagen",
        "de": "In den Warenkorb",
        "fa": "افزودن به سبد"
    },
    "login_to_buy": {
        "fr": "Connectez-vous pour acheter",
        "en": "Login to buy",
        "nl": "Log in om te kopen",
        "de": "Anmelden zum Kaufen",
        "fa": "برای خرید وارد شوید"
    },
    "no_description": {
        "fr": "Aucune description",
        "en": "No description",
        "nl": "Geen beschrijving",
        "de": "Keine Beschreibung",
        "fa": "بدون توضیحات"
    },

    # ========== Auth ==========
    "username": {
        "fr": "Nom d'utilisateur",
        "en": "Username",
        "nl": "Gebruikersnaam",
        "de": "Benutzername",
        "fa": "نام کاربری"
    },
    "email": {
        "fr": "E-mail",
        "en": "Email",
        "nl": "E-mail",
        "de": "E-Mail",
        "fa": "ایمیل"
    },
    "password": {
        "fr": "Mot de passe",
        "en": "Password",
        "nl": "Wachtwoord",
        "de": "Passwort",
        "fa": "رمز عبور"
    },
    "want_to_be_seller": {
        "fr": "Je souhaite vendre mes propres articles",
        "en": "I want to sell my own items",
        "nl": "Ik wil mijn eigen artikelen verkopen",
        "de": "Ich möchte meine eigenen Artikel verkaufen",
        "fa": "می‌خواهم فروشنده باشم (اجناس خودم را بفروشم)"
    },
    "already_registered": {
        "fr": "Déjà inscrit ?",
        "en": "Already registered?",
        "nl": "Al geregistreerd?",
        "de": "Bereits registriert?",
        "fa": "قبلاً ثبت‌نام کرده‌اید؟"
    },
    "no_account": {
        "fr": "Pas encore de compte ?",
        "en": "Don't have an account?",
        "nl": "Nog geen account?",
        "de": "Noch kein Konto?",
        "fa": "حساب ندارید؟"
    },
    "please_login": {
        "fr": "Veuillez vous connecter.",
        "en": "Please log in.",
        "nl": "Log alstublieft in.",
        "de": "Bitte melden Sie sich an.",
        "fa": "لطفاً ابتدا وارد شوید."
    },

    # ========== Cart ==========
    "product": {
        "fr": "Produit",
        "en": "Product",
        "nl": "Product",
        "de": "Produkt",
        "fa": "محصول"
    },
    "price": {
        "fr": "Prix",
        "en": "Price",
        "nl": "Prijs",
        "de": "Preis",
        "fa": "قیمت"
    },
    "quantity": {
        "fr": "Quantité",
        "en": "Quantity",
        "nl": "Aantal",
        "de": "Menge",
        "fa": "تعداد"
    },
    "subtotal": {
        "fr": "Sous-total",
        "en": "Subtotal",
        "nl": "Subtotaal",
        "de": "Zwischensumme",
        "fa": "جمع"
    },
    "total": {
        "fr": "Total",
        "en": "Total",
        "nl": "Totaal",
        "de": "Gesamt",
        "fa": "جمع کل"
    },
    "update": {
        "fr": "Mettre à jour",
        "en": "Update",
        "nl": "Bijwerken",
        "de": "Aktualisieren",
        "fa": "به‌روز"
    },
    "pay_with_stripe": {
        "fr": "Payer avec Stripe",
        "en": "Pay with Stripe",
        "nl": "Betalen met Stripe",
        "de": "Mit Stripe bezahlen",
        "fa": "پرداخت با Stripe"
    },
    "cart_empty": {
        "fr": "Votre panier est vide.",
        "en": "Your cart is empty.",
        "nl": "Je winkelwagen is leeg.",
        "de": "Ihr Warenkorb ist leer.",
        "fa": "سبد خرید شما خالی است."
    },
    "browse_products": {
        "fr": "Parcourir les produits",
        "en": "Browse products",
        "nl": "Producten bekijken",
        "de": "Produkte durchsuchen",
        "fa": "مشاهده محصولات"
    },

    # ========== Seller ==========
    "new_product": {
        "fr": "Nouveau produit",
        "en": "New product",
        "nl": "Nieuw product",
        "de": "Neues Produkt",
        "fa": "محصول جدید"
    },
    "my_sales": {
        "fr": "Mes ventes",
        "en": "My sales",
        "nl": "Mijn verkopen",
        "de": "Meine Verkäufe",
        "fa": "سفارش‌های من"
    },
    "connect_stripe": {
        "fr": "Connecter Stripe",
        "en": "Connect Stripe",
        "nl": "Stripe verbinden",
        "de": "Stripe verbinden",
        "fa": "اتصال به Stripe"
    },
    "stripe_connect_needed": {
        "fr": "Pour recevoir vos paiements, connectez votre compte Stripe.",
        "en": "To receive payments, connect your Stripe account.",
        "nl": "Om betalingen te ontvangen, verbind je Stripe-account.",
        "de": "Um Zahlungen zu erhalten, verbinden Sie Ihr Stripe-Konto.",
        "fa": "برای دریافت پول، حساب Stripe را متصل کنید."
    },
    "stripe_connected": {
        "fr": "Votre compte Stripe est connecté et actif.",
        "en": "Your Stripe account is connected and active.",
        "nl": "Je Stripe-account is verbonden en actief.",
        "de": "Ihr Stripe-Konto ist verbunden und aktiv.",
        "fa": "حساب Stripe شما متصل و فعال است."
    },
    "total_sales": {
        "fr": "Ventes totales",
        "en": "Total sales",
        "nl": "Totale verkopen",
        "de": "Gesamtumsatz",
        "fa": "کل فروش"
    },
    "products_count": {
        "fr": "Nombre de produits",
        "en": "Number of products",
        "nl": "Aantal producten",
        "de": "Anzahl der Produkte",
        "fa": "تعداد محصولات"
    },
    "my_products": {
        "fr": "Mes produits",
        "en": "My products",
        "nl": "Mijn producten",
        "de": "Meine Produkte",
        "fa": "محصولات من"
    },
    "status": {
        "fr": "Statut",
        "en": "Status",
        "nl": "Status",
        "de": "Status",
        "fa": "وضعیت"
    },
    "active": {
        "fr": "Actif",
        "en": "Active",
        "nl": "Actief",
        "de": "Aktiv",
        "fa": "فعال"
    },
    "inactive": {
        "fr": "Inactif",
        "en": "Inactive",
        "nl": "Inactief",
        "de": "Inaktiv",
        "fa": "غیرفعال"
    },
    "actions": {
        "fr": "Actions",
        "en": "Actions",
        "nl": "Acties",
        "de": "Aktionen",
        "fa": "عملیات"
    },
    "edit": {
        "fr": "Modifier",
        "en": "Edit",
        "nl": "Bewerken",
        "de": "Bearbeiten",
        "fa": "ویرایش"
    },
    "delete": {
        "fr": "Supprimer",
        "en": "Delete",
        "nl": "Verwijderen",
        "de": "Löschen",
        "fa": "حذف"
    },
    "no_products_yet": {
        "fr": "Vous n'avez pas encore de produits.",
        "en": "You have no products yet.",
        "nl": "Je hebt nog geen producten.",
        "de": "Sie haben noch keine Produkte.",
        "fa": "هنوز محصولی ندارید."
    },
    "add_product": {
        "fr": "Ajouter un produit",
        "en": "Add a product",
        "nl": "Product toevoegen",
        "de": "Produkt hinzufügen",
        "fa": "افزودن محصول"
    },
    "product_name": {
        "fr": "Nom du produit",
        "en": "Product name",
        "nl": "Productnaam",
        "de": "Produktname",
        "fa": "نام محصول"
    },
    "description": {
        "fr": "Description",
        "en": "Description",
        "nl": "Beschrijving",
        "de": "Beschreibung",
        "fa": "توضیحات"
    },
    "price_usd": {
        "fr": "Prix (USD)",
        "en": "Price (USD)",
        "nl": "Prijs (USD)",
        "de": "Preis (USD)",
        "fa": "قیمت (دلار)"
    },
    "product_image": {
        "fr": "Image du produit",
        "en": "Product image",
        "nl": "Productafbeelding",
        "de": "Produktbild",
        "fa": "تصویر محصول"
    },
    "save_product": {
        "fr": "Enregistrer le produit",
        "en": "Save product",
        "nl": "Product opslaan",
        "de": "Produkt speichern",
        "fa": "ذخیره محصول"
    },
    "cancel": {
        "fr": "Annuler",
        "en": "Cancel",
        "nl": "Annuleren",
        "de": "Abbrechen",
        "fa": "انصراف"
    },
    "edit_product": {
        "fr": "Modifier le produit",
        "en": "Edit product",
        "nl": "Product bewerken",
        "de": "Produkt bearbeiten",
        "fa": "ویرایش محصول"
    },
    "save_changes": {
        "fr": "Enregistrer les modifications",
        "en": "Save changes",
        "nl": "Wijzigingen opslaan",
        "de": "Änderungen speichern",
        "fa": "ذخیره تغییرات"
    },
    "keep_active": {
        "fr": "Garder actif",
        "en": "Keep active",
        "nl": "Actief houden",
        "de": "Aktiv lassen",
        "fa": "فعال باشد"
    },

    # ========== Orders & Checkout ==========
    "payment_success": {
        "fr": "Paiement réussi !",
        "en": "Payment successful!",
        "nl": "Betaling geslaagd!",
        "de": "Zahlung erfolgreich!",
        "fa": "پرداخت با موفقیت انجام شد!"
    },
    "order_number": {
        "fr": "Numéro de commande",
        "en": "Order number",
        "nl": "Bestelnummer",
        "de": "Bestellnummer",
        "fa": "شماره سفارش"
    },
    "amount": {
        "fr": "Montant",
        "en": "Amount",
        "nl": "Bedrag",
        "de": "Betrag",
        "fa": "مبلغ"
    },
    "view_orders": {
        "fr": "Voir mes commandes",
        "en": "View my orders",
        "nl": "Mijn bestellingen bekijken",
        "de": "Meine Bestellungen ansehen",
        "fa": "مشاهده سفارش‌ها"
    },
    "back_to_shop": {
        "fr": "Retour à la boutique",
        "en": "Back to shop",
        "nl": "Terug naar de winkel",
        "de": "Zurück zum Shop",
        "fa": "بازگشت به فروشگاه"
    },
    "no_orders": {
        "fr": "Vous n'avez pas encore de commandes.",
        "en": "You have no orders yet.",
        "nl": "Je hebt nog geen bestellingen.",
        "de": "Sie haben noch keine Bestellungen.",
        "fa": "هنوز سفارشی ندارید."
    },
    "received_orders": {
        "fr": "Commandes reçues",
        "en": "Received orders",
        "nl": "Ontvangen bestellingen",
        "de": "Eingegangene Bestellungen",
        "fa": "سفارش‌های دریافتی"
    },
    "no_sales_yet": {
        "fr": "Vous n'avez pas encore de ventes.",
        "en": "You have no sales yet.",
        "nl": "Je hebt nog geen verkopen.",
        "de": "Sie haben noch keine Verkäufe.",
        "fa": "هنوز فروشی نداشته‌اید."
    },
    "stripe_transfer": {
        "fr": "Transfert Stripe",
        "en": "Stripe transfer",
        "nl": "Stripe-overdracht",
        "de": "Stripe-Überweisung",
        "fa": "انتقال Stripe"
    },
    "pending": {
        "fr": "En attente",
        "en": "Pending",
        "nl": "In afwachting",
        "de": "Ausstehend",
        "fa": "در انتظار"
    },
    "date": {
        "fr": "Date",
        "en": "Date",
        "nl": "Datum",
        "de": "Datum",
        "fa": "تاریخ"
    },

    # ========== Admin ==========
    "admin_panel": {
        "fr": "Panneau d'administration",
        "en": "Admin Panel",
        "nl": "Beheerderspaneel",
        "de": "Admin-Bereich",
        "fa": "پنل ادمین"
    },
    "users": {
        "fr": "Utilisateurs",
        "en": "Users",
        "nl": "Gebruikers",
        "de": "Benutzer",
        "fa": "کاربران"
    },
    "products": {
        "fr": "Produits",
        "en": "Products",
        "nl": "Producten",
        "de": "Produkte",
        "fa": "محصولات"
    },
    "recent_orders": {
        "fr": "Commandes récentes",
        "en": "Recent orders",
        "nl": "Recente bestellingen",
        "de": "Aktuelle Bestellungen",
        "fa": "آخرین سفارش‌ها"
    },

    # ========== Footer & Misc ==========
    "footer_text": {
        "fr": "Ramos — Marketplace multi-vendeurs avec Stripe | Propulsé par Flask",
        "en": "Ramos — Multi-vendor marketplace with Stripe | Powered by Flask",
        "nl": "Ramos — Multi-vendor marketplace met Stripe | Aangedreven door Flask",
        "de": "Ramos — Multi-Vendor-Marktplatz mit Stripe | Powered by Flask",
        "fa": "Ramos — فروشگاه چندفروشنده‌ای با Stripe | ساخته شده با Flask"
    },



    "share": {
        "fr": "Partager",
        "en": "Share",
        "nl": "Delen",
        "de": "Teilen",
        "fa": "اشتراک‌گذاری"
    },
    "copy_link": {
        "fr": "Copier le lien",
        "en": "Copy link",
        "nl": "Link kopiëren",
        "de": "Link kopieren",
        "fa": "کپی لینک"
    },
    "product_images": {
        "fr": "Photos du produit",
        "en": "Product photos",
        "nl": "Productfoto's",
        "de": "Produktfotos",
        "fa": "عکس‌های محصول"
    },
    "images_hint": {
        "fr": "JPG, PNG, WEBP ou GIF — max 5 photos, ~5 Mo chacune (photo téléphone).",
        "en": "JPG, PNG, WEBP or GIF — max 5 photos, ~5 MB each (phone camera).",
        "nl": "JPG, PNG, WEBP of GIF — max 5 foto's, ~5 MB per stuk.",
        "de": "JPG, PNG, WEBP oder GIF — max. 5 Fotos, ca. 5 MB je Stück.",
        "fa": "فقط JPG، PNG، WEBP یا GIF — حداکثر ۵ عکس، حدود ۵ مگابایت هر کدام (عکس گوشی)."
    },
    "current_images": {
        "fr": "Photos actuelles",
        "en": "Current photos",
        "nl": "Huidige foto's",
        "de": "Aktuelle Fotos",
        "fa": "عکس‌های فعلی"
    },
    "add_more_images": {
        "fr": "Ajouter d'autres photos",
        "en": "Add more photos",
        "nl": "Meer foto's toevoegen",
        "de": "Weitere Fotos hinzufügen",
        "fa": "افزودن عکس بیشتر"
    },
    "become_seller": {
        "fr": "Devenir vendeur",
        "en": "Become a seller",
        "nl": "Verkoper worden",
        "de": "Verkäufer werden",
        "fa": "فروشنده شو"
    },
    "login_with_google": {
        "fr": "Continuer avec Google",
        "en": "Continue with Google",
        "nl": "Doorgaan met Google",
        "de": "Weiter mit Google",
        "fa": "ادامه با گوگل"
    },
    "or": {
        "fr": "ou",
        "en": "or",
        "nl": "of",
        "de": "oder",
        "fa": "یا"
    },
    "language": {
        "fr": "Langue",
        "en": "Language",
        "nl": "Taal",
        "de": "Sprache",
        "fa": "زبان"
    },
}

SUPPORTED_LANGUAGES = {
    "fr": "Français",
    "en": "English",
    "nl": "Nederlands",
    "de": "Deutsch",
    "fa": "فارسی",
}

DEFAULT_LANGUAGE = "fr"


def get_translation(key: str, lang: str = None) -> str:
    """Get translated string for the given key and language."""
    if lang is None:
        lang = DEFAULT_LANGUAGE
    entry = TRANSLATIONS.get(key)
    if not entry:
        return key
    return entry.get(lang) or entry.get(DEFAULT_LANGUAGE) or key
