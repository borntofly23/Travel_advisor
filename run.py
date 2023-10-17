# Flask application

from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import jwt
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import json
from bson import json_util
from bson.json_util import dumps
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Secret key
app.secret_key = 'secretkey'

# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['trip_advisor']

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
           return jsonify({'message': 'Token is missing!'}), 403
        try:
           data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
           return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated

# Create route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = db.users.find_one({'email': request.form['email']})
        if user:
            if check_password_hash(user['password'], request.form['password']):
                flash('Logged in successfully')
                return render_template('home.html')
            else:
                flash('Incorrect password')
                return render_template('login.html')
        else:
            flash('Email does not exist')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        user = db.users.find_one({'email': request.form['email']})
        if user:
            flash('Email already exists')
            return render_template('register.html')
        else:
            db.users.insert_one({
                'name': request.form['name'],
                'email': request.form['email'],
                'number': request.form['number'],
                'state': request.form['state'],
                'password': generate_password_hash(request.form['password'])
            })
            flash('User successfully registered')
        return render_template('register.html')
    else:
        return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
