# 🍪 Cookie-Craft

Cookie-Craft is a secure, full-featured Flask web app for user authentication and session-based access. It includes login, registration, admin control, and user profile management.

---

## 🚀 Features

- 🔐 User registration, login, and logout
- 🧂 Password hashing with Werkzeug
- 👤 Profile page (editable username & bio)
- 🛒 Protected shop page (requires login)
- 👑 Admin panel (`/admin/users`) to view users
- ⚠️ Flash message notifications
- 🧠 Session-based login with Flask-Login
- 📦 SQLite for storage

---

## 🧰 Tech Stack

- Python 3.12+
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Werkzeug
- Python-dotenv (for environment variables)

---

## 📦 Installation

### 1. To run it

```bash
git clone https://github.com/yourusername/cookie-craft.git
cd cookie-craft/app
pip install flask flask_sqlalchemy flask_login werkzeug python-dotenv
python app.py








