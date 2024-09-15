#importing necessary libraries
import requests
import json
import sqlite3
from datetime import datetime
import google.generativeai as genai
import os

#fitbit api token
FITBIT_API_URL = "https://api.fitbit.com/1/user/-/"
TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1BMRDkiLCJzdWIiOiJDN1o0MzciLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3bnV0IHdzbGUgd3dlaSB3c29jIHdhY3Qgd3NldCB3bG9jIiwiZXhwIjoxNzI2NDcyMDA4LCJpYXQiOjE3MjYzODU2MDh9.GGLnqigz-AbrmPM4GmTysIjOEz8Tax1FLtSFl4E3HaQ"  # Replace with your Fitbit access token

#authorization
headers = {
    "Authorization": f"Bearer {TOKEN}"
}
#google generative ai open source key
os.environ["API_KEY"] = "AIzaSyAsDHVYYQXCqlzxgINN_9QE2g65QLFh0Ew"
genai.configure(api_key=os.environ["API_KEY"])

#sql database to store the fetched data
conn = sqlite3.connect('fitness_data.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS fitbit_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    steps INTEGER,
    calories_burned INTEGER,
    calories_consumed INTEGER,
    sleep_duration INTEGER,
    active_minutes INTEGER,
    distance REAL,
    floors_climbed INTEGER
)
''')
conn.commit()

#fetch data from fitbit api
def fetch_fitbit_data():
    try:
        #daily activity summary (steps, calories burned)
        activity_url = f"{FITBIT_API_URL}activities/date/today.json"
        activity_data = requests.get(activity_url, headers=headers).json()

        #fetch sleep time
        sleep_url = f"{FITBIT_API_URL}sleep/date/today.json"
        sleep_data = requests.get(sleep_url, headers=headers).json()

        #fetch nutrition (calories consumed)
        food_url = f"{FITBIT_API_URL}foods/log/date/today.json"
        food_data = requests.get(food_url, headers=headers).json()

        #fetching only relevant data
        filtered_data = {
            "date": str(datetime.today().date()),
            "steps": activity_data.get("summary", {}).get("steps", 0),
            "calories_burned": activity_data.get("summary", {}).get("caloriesOut", 0),
            "calories_consumed": food_data.get("summary", {}).get("calories", 0),
            "sleep_duration": sleep_data.get("summary", {}).get("totalMinutesAsleep", 0),
            "active_minutes": activity_data.get("summary", {}).get("fairlyActiveMinutes", 0) + activity_data.get("summary", {}).get("veryActiveMinutes", 0),
            "distance": activity_data.get("summary", {}).get("distances", [{}])[0].get("distance", 0.0),
            "floors_climbed": activity_data.get("summary", {}).get("floors", 0)
        }

        return filtered_data

    except Exception as e:
        print(f"Error fetching Fitbit data: {e}")
        return None

#store data into the created sql database
def store_fitbit_data(fitbit_data):
    if fitbit_data:
        #check if data for today is already in the database
        cursor.execute('SELECT * FROM fitbit_data WHERE date = ?', (fitbit_data['date'],))
        existing_data = cursor.fetchone()

        if existing_data:
            print("Data for today is already stored.")
        else:
            #insert new data into database
            cursor.execute('''
                INSERT INTO fitbit_data (
                    date, steps, calories_burned, calories_consumed, sleep_duration, 
                    active_minutes, distance, floors_climbed
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                fitbit_data['date'], fitbit_data['steps'], fitbit_data['calories_burned'],
                fitbit_data['calories_consumed'], fitbit_data['sleep_duration'],
                fitbit_data['active_minutes'],
                fitbit_data['distance'], fitbit_data['floors_climbed']
            ))
            conn.commit()
            print(f"Data for {fitbit_data['date']} has been stored.")

#main function
if __name__ == "__main__":

    fitbit_data = fetch_fitbit_data()

    if fitbit_data:
        #print fetched user data
        print("\nFetched Fitbit Data: ")
        print(json.dumps(fitbit_data, indent=4))
        store_fitbit_data(fitbit_data)

    conn.close()