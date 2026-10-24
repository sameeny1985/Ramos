# Ramos — Marketplace multi-vendeurs (Flask + Stripe)

**Site en français par défaut** avec support multilingue complet :

| Langue     | Code |
|------------|------|
| Français   | `fr` (défaut) |
| English    | `en` |
| Nederlands | `nl` |
| Deutsch    | `de` |
| فارسی      | `fa` |

## Connexion admin

- **Email admin:** `shapyaar@gmail.com`
- ورود با **Google OAuth** (دکمه Continue with Google → لیست اکانت‌های گوگل نمایش داده می‌شود)
- وقتی با همین ایمیل گوگل لاگین کنید، خودکار ادمین می‌شوید.

## Fonctionnalités

- Inscription / connexion
- Rôle vendeur : les utilisateurs peuvent vendre leurs propres articles
- Panier + commandes
- Paiement sécurisé **Stripe Checkout** (EUR)
- **Stripe Connect** (Express) pour payer les vendeurs
- Commission plateforme configurable
- Switcher de langue dans la navbar
- RTL automatique pour le persan
- Prêt pour GitHub + Render

## Démarrage local

```bash
cd marketplace
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Renseigner les clés Stripe
python app.py
```

→ http://localhost:5000

**Admin :** `admin@example.com` / `admin123`

## Déploiement Render

1. Push sur GitHub
2. Render → New Blueprint → sélectionner le repo (`render.yaml`)
3. Renseigner les variables Stripe + `APP_URL`
4. Deploy !

## Structure des traductions

Toutes les chaînes sont dans `translations.py`.  
Pour ajouter une langue, ajoutez simplement les clés dans le dictionnaire.

## Notes

- Devise : **EUR**
- Pays Stripe Connect par défaut : **FR**
- Langue par défaut : **Français**
