from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

import os

app = Flask(__name__,
            template_folder=os.path.abspath('./client/templates'),
            static_folder=os.path.abspath('./static'))
app.secret_key = 'your_secret_key'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # ... your validation code ...

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')


# Login: check hashed password
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password')

    return render_template('login.html')

@app.route('/admin/users')
def list_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/reset_password')
def reset_password():
    return render_template('reset_password.html')

# ✅ This should come LAST
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
