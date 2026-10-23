import requests
import os

FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")

def password_reset(payload):
    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_WEB_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "requestType": "PASSWORD_RESET",
        "email": payload.email
    }
    response = requests.post(rest_api_url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()
