# Django Marketplace

A full-featured marketplace web application built with Django, where users can browse listings, view item details, register as buyers or sellers, manage their profiles, and contact sellers directly through an in-app messaging system.

---

## Features

- **Browse Listings** — View all available items in a responsive card grid with category filtering
- **Item Detail Pages** — See full item info, seller contact details, and send messages
- **User Authentication** — Register, log in, and log out securely
- **Seller Profiles** — Public profile pages showing seller info and their active listings
- **Edit Profile** — Update username, email, bio, phone number, and location
- **In-App Messaging** — Buyers can contact sellers directly from item pages
- **Inbox** — View received and sent messages with read/unread tracking
- **Django Admin** — Full admin panel for managing items, users, and messages
- **Responsive UI** — Works on desktop and mobile

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.14, Django 6.0 |
| Database | SQLite (development) |
| Frontend | HTML, CSS, JavaScript (no framework) |
| Auth | Django's built-in authentication system |
| Styling | Custom CSS with CSS variables |
| Fonts | Google Fonts (Playfair Display, DM Sans) |

---

## Project Structure

marketplace/
├── core/                   # Project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── listings/               # Marketplace listings app
│   ├── models.py           # Item, Message models
│   ├── views.py            # item_list, item_detail, send_message, inbox
│   ├── urls.py
│   ├── forms.py            # MessageForm
│   ├── admin.py
│   └── templates/
│       └── listings/
│           ├── base.html
│           ├── item_list.html
│           ├── item_detail.html
│           └── inbox.html
├── users/                  # User auth and profiles app
│   ├── models.py           # Profile model
│   ├── views.py            # register, login, logout, profile, edit_profile
│   ├── urls.py
│   ├── forms.py            # RegisterForm, UserUpdateForm, ProfileUpdateForm
│   ├── signals.py          # Auto-create profile on user registration
│   ├── admin.py
│   └── templates/
│       └── users/
│           ├── register.html
│           ├── login.html
│           ├── profile.html
│           └── edit_profile.html
├── manage.py
├── db.sqlite3
└── README.md
```

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/django-marketplace.git
cd django-marketplace
```

### 2. Create and activate a virtual environment

```bash
# Windows (PowerShell)
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install django
```

### 4. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

---

## Pages & URLs

| URL | Page | Access |
|---|---|---|
| `/` | Browse all listings | Public |
| `/item/<id>/` | Item detail page | Public |
| `/item/<id>/message/` | Send message to seller | Login required |
| `/inbox/` | View messages | Login required |
| `/users/register/` | Create an account | Public |
| `/users/login/` | Sign in | Public |
| `/users/logout/` | Sign out | Login required |
| `/users/profile/<username>/` | View a user's profile | Public |
| `/users/profile/edit/` | Edit your profile | Login required |
| `/admin/` | Django admin panel | Superuser only |

---

## Data Models

### `Item` (listings app)
| Field | Type | Description |
|---|---|---|
| `name` | CharField | Name of the item |
| `description` | TextField | Full item description |
| `price` | DecimalField | Listing price |
| `category` | CharField | electronics / clothing / furniture / other |
| `image_url` | URLField | Optional image link |
| `is_available` | BooleanField | Whether item is still for sale |
| `seller` | ForeignKey (User) | The user who posted the item |
| `created_at` | DateTimeField | When the listing was created |

### `Message` (listings app)
| Field | Type | Description |
|---|---|---|
| `item` | ForeignKey (Item) | The item being enquired about |
| `sender` | ForeignKey (User) | Who sent the message |
| `receiver` | ForeignKey (User) | Who receives the message |
| `body` | TextField | The message content |
| `is_read` | BooleanField | Whether the message has been read |
| `created_at` | DateTimeField | When the message was sent |

### `Profile` (users app)
| Field | Type | Description |
|---|---|---|
| `user` | OneToOneField (User) | Linked Django user |
| `bio` | TextField | Short seller/buyer bio |
| `phone` | CharField | Contact phone number |
| `location` | CharField | City or region |
| `profile_picture` | URLField | Optional avatar image URL |

---

## Running Tests

```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test listings
python manage.py test users
```

---

## Environment & Security Notes

- `DEBUG = True` is set for development only — set to `False` in production
- `SECRET_KEY` should be moved to an environment variable before deploying
- SQLite is used for development — switch to PostgreSQL for production
- No file upload support yet — item images are added via URL

---

## Potential Future Improvements

- [ ] Real-time chat with Django Channels + WebSockets
- [ ] Email notifications when a new message is received
- [ ] Image file uploads using `ImageField` + Pillow
- [ ] Search and advanced filtering (price range, location)
- [ ] Seller ratings and reviews
- [ ] Pagination for large listing pages
- [ ] Password reset via email
- [ ] Deployment to a platform like Railway or Render

---

## Author

**Gideon**
Built as a learning project to explore Django's core features including models, views, templates, authentication, signals, and forms.

---

## License

This project is open source and available under the [MIT License](LICENSE).