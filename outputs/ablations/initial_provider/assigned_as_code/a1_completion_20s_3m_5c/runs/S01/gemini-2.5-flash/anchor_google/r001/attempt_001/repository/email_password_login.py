import requests
import os

FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")

def email_password_login(payload):
    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "email": payload.email,
        "password": payload.password,
        "returnSecureToken": True
    }
    response = requests.post(rest_api_url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()
