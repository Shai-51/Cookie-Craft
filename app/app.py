# Import necessary modules and extensions
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os
import secrets

# Initialize the Flask app with custom paths for templates and static files
app = Flask(__name__,
            template_folder=os.path.abspath('./client/templates'),
            static_folder=os.path.abspath('./static'))

# Set a secure secret key for sessions and cookies
app.secret_key = secrets.token_hex(32)

# Configure SQLite database settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy for ORM support
db = SQLAlchemy(app)

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to 'login' route if user is not authenticated

# Define the User model using SQLAlchemy and UserMixin for Flask-Login compatibility
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each user
    username = db.Column(db.String(80), unique=False, nullable=False)  # Display name
    email = db.Column(db.String(120), unique=True, nullable=False)  # User's email (must be unique)
    password = db.Column(db.String(120), nullable=False)  # Hashed password
    is_admin = db.Column(db.Boolean, default=False)  # Admin flag
    bio = db.Column(db.Text, default='')  # Optional user bio

# Define user loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Fetch user from DB by ID

# Home route — accessible to everyone
@app.route('/')
def home():
    return render_template('index.html')  # Render homepage

# Friend list route — requires login
@app.route('/friends')
@login_required
def friend():
    users = User.query.all()  # Get all users from database
    return render_template('friend.html', users=users)  # Show friend list

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Basic validation
        if not username or not email or not password:
            flash('All fields are required!')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('register'))

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered!')
            return redirect(url_for('register'))

        # Hash the password before saving
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)

        # Add new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')  # Render registration form

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))  # Prevent re-login if already authenticated

    if request.method == 'POST':
        # Retrieve submitted credentials
        email = request.form.get('email')
        password = request.form.get('password')

        # Attempt to find user and verify password
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)  # Log in the user
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password')  # Show error if login fails

    return render_template('login.html')  # Render login form

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()  # End user session
    flash('Logged out successfully.')
    return redirect(url_for('home'))

# Admin panel for viewing all users — restricted to admin users only
@app.route('/admin/users')
@login_required
def list_users():
    if not current_user.is_admin:
        flash("You do not have permission to access this page.")
        return redirect(url_for('home'))
    users = User.query.all()
    return render_template('admin_users.html', users=users)

# Password reset page (placeholder for now)
@app.route('/reset_password')
def reset_password():
    return render_template('reset_password.html')

# Profile management route
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Get updated info from form
        new_username = request.form.get('username')
        new_bio = request.form.get('bio')

        # Update current user's profile
        current_user.username = new_username
        current_user.bio = new_bio
        db.session.commit()

        flash("Profile updated successfully!")
        return redirect(url_for('profile'))

    return render_template('profile.html', user=current_user)  # Display profile page

# Main entry point
if __name__ == '__main__':
    # Create all database tables if they don't exist
    with app.app_context():
        db.create_all()

    # Run the Flask app on all IPs at port 5000 with debug mode on
    app.run(host="0.0.0.0", debug=True)
