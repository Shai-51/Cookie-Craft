from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__,
            template_folder=os.path.abspath('./client/templates'),
            static_folder=os.path.abspath('./static'))
app.secret_key = 'your_secret_key'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/shop')
def shop():
    return render_template('shop.html')


@app.route('/login', methods=['GET', 'POS T'])
def login():
    if request.method == 'POST':
        # Placeholder login logic
        email = request.form['email']
        password = request.form['password']

        # You can replace this with your own logic later
        if email == 'test@example.com' and password == 'password':
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not username or not email or not password:
            flash('All fields are required!')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('register'))

        # Placeholder: pretend registration succeeded
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/reset_password')
def reset_password():
    return render_template('reset_password.html')


if __name__ == '__main__':
    app.run(debug=True)
