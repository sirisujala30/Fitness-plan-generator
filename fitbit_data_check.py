#importing necessary libraries
import requests
import json

#fibit api tokens
FITBIT_API_URL = "https://api.fitbit.com/1/user/-/"
TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1BMRDkiLCJzdWIiOiJDN1o0MzciLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3bnV0IHdzbGUgd3dlaSB3c29jIHdhY3Qgd3NldCB3bG9jIiwiZXhwIjoxNzI2NDcyMDA4LCJpYXQiOjE3MjYzODU2MDh9.GGLnqigz-AbrmPM4GmTysIjOEz8Tax1FLtSFl4E3HaQ"  # Replace with your Fitbit access token

#authorization
headers = {
    "Authorization": f"Bearer {TOKEN}"
}

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

        return {
            "activity": activity_data,
            "sleep": sleep_data,
            "nutrition": food_data
        }
    except Exception as e:
        print(f"Error fetching Fitbit data: {e}")
        return None

#main function
if __name__ == "__main__":

    fitbit_data = fetch_fitbit_data()

    if fitbit_data:
        #print fetched user data
        print("\nFetched Fitbit Data: ")
        print(json.dumps(fitbit_data, indent=4))
    else:
        print("Failed to fetch Fitbit data.")
