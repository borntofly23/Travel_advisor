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
import requests
from datetime import datetime, date, timedelta

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
                return redirect('/home')
            else:
                flash('Incorrect password')
                return render_template('login.html')
        else:
            flash('Email does not exist')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/home', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        details = request.form['subject']
        # flights = requests.get("https://tripadvisor16.p.rapidapi.com/api/v1/flights/searchAirport",
        #                         headers = {
        #                             'X-RapidAPI-Key': '14cb89a0e8mshe01e8ebf6bb311ap1caf5fjsnb60ad9d3484b',
        #                             'X-RapidAPI-Host': 'tripadvisor16.p.rapidapi.com'
        #                         }, params={"query":details}).json()['data']
        # if len(flights) == 0:
        #     flash('No flights found')
        #     return redirect('/home')

        # weather = requests.get("https://weatherapi-com.p.rapidapi.com/current.json", headers={
        #     "X-RapidAPI-Key": "64506c4a2cmsh6ec927e08a29bb7p1a899djsn638614c3fbb1",
        #     "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
        # }, params={"q":details,"days":"1"}).json()

        location = requests.get("https://booking-com.p.rapidapi.com/v1/hotels/locations",
                                headers = {
                                            "X-RapidAPI-Key": "64506c4a2cmsh6ec927e08a29bb7p1a899djsn638614c3fbb1",
                                            "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
                                }, params={"name":details,"locale":"en-us"}).json()[0]
        
        location = {
            'dest_id': location['dest_id'],
            'dest_type': location['dest_type'],
            'longitude': location['longitude'],
            'latitude': location['latitude'],
            'country': location['cc1'],
        }

        # hotels = requests.get("https://booking-com.p.rapidapi.com/v1/hotels/search", headers={
        #             "X-RapidAPI-Key": "64506c4a2cmsh6ec927e08a29bb7p1a899djsn638614c3fbb1",
        #             "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
        #         }, params={"checkin_date":date.today()  + timedelta(days=1),"dest_type":"city","units":"metric",
        #                 "checkout_date":date.today()  + timedelta(days=2),
        #                 "adults_number":"1","order_by":"popularity", "dest_id":location['dest_id'],"filter_by_currency":"INR",
        #                 "locale":"en-us","room_number":"1"}).json()['result']
        # if len(hotels) > 12:
        #     hotels = hotels[:12]
        
        return render_template('details.html', data={
            # 'flight': flights,
            # 'weather': weather,
            'location': location,
            # 'hotels': hotels,
            'count': {
                # 'airports': len(flights),
                # 'hotels': len(hotels),
            },
        })
    elif request.method == "GET":
        return render_template('home.html')

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
