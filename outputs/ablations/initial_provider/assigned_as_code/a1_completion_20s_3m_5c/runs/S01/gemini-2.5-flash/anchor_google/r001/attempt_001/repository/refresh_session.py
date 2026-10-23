import requests
import os

FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")

def refresh_session(payload):
    rest_api_url = f"https://securetoken.googleapis.com/v1/token?key={FIREBASE_WEB_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "grant_type": "refresh_token",
        "refresh_token": payload.refresh_token
    }
    response = requests.post(rest_api_url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()
