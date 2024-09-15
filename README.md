# Fitness-plan-generator

## Overview: 
The Dynamic Fitness Plan Generator is designed to create personalized workout plans using real-time data from wearable devices such as Fitbit. It dynamically adjusts the user's workout routine based on their performance data, such as steps taken, calories burned, sleep patterns, and nutrition intake. The system leverages Fitbit's API for retrieving fitness data and Google Generative AI for generating customized workout plans based on user goals, preferences, and available data.

## Features
- **Wearable Device Integration**: Fetch real-time fitness data (steps, calories burned, sleep duration) via the Fitbit API.
- **Dynamic Workout Plan Generation**: Google Generative AI generates workout routines tailored to user fitness data and goals.
- **Customizable Plans**: Users can specify their goals (e.g., weight loss, muscle gain), workout preferences, available equipment, and dietary preferences.
- **PDF Export**: Automatically generates a downloadable PDF of the workout plan.

## Prerequisites
- Python 3.x
- Fitbit account with access token
- Google Generative AI API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sirisujala30/fitness-plan-generator.git

## Configuration
1. Replace your Fitbit API token in the code:
```python
TOKEN = "your_fitbit_api_token"
```

2. Set up your Google Generative AI API key:
```python
os.environ["API_KEY"] = "your_google_api_key"
```

## Usage
```bash
strealmit run workout_generator.py
