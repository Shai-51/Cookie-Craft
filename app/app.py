from flask import Flask, render_template
import os

app = Flask(__name__,
            template_folder=os.path.abspath('./client/templates'),
            static_folder=os.path.abspath('./static'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/reset_password')
def reset_password():
    return render_template('reset_password.html')

if __name__ == '__main__':
    app.run(debug=True)
