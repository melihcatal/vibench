import os
import requests


FIREBASE_PROJECT_ID = os.environ["FIREBASE_PROJECT_ID"]
FIREBASE_WEB_API_KEY = os.environ["FIREBASE_WEB_API_KEY"]


def register_user(email: str, password: str) -> dict:
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_WEB_API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True,
    }
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    data["firebaseProjectId"] = FIREBASE_PROJECT_ID
    return data
