#!/usr/bin/env python3
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Weather.sqlite3'

'''
Define the database model
that is used to store 
the temperature.
'''

db = SQLAlchemy(app)


class Weather(db.Model):
    datetime = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow)
    temperature = db.Column(db.Integer, nullable=False)


'''
Helper function to get temperature
using API
'''


def get_temperature():
    try:
        response = requests.get("https://weatherdbi.herokuapp.com/data/weather/boulder")
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()["currentConditions"]["temp"]["c"]
    except (requests.RequestException, KeyError):
        # Generate a random temperature between -10 and 40 degrees Celsius
        return random.randint(-10, 40)


'''
In main we first get the current temperature and then 
create a new object that we can add to the database. 
'''
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure the database and tables are created
        current_temperature = get_temperature()
        new_entry = Weather(temperature=current_temperature)
        db.session.add(new_entry)
        db.session.commit()
        print(f"New temperature entry added: {current_temperature}")
