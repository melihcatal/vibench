import os
import requests


FIREBASE_PROJECT_ID = os.environ["FIREBASE_PROJECT_ID"]
FIREBASE_API_KEY = os.environ["FIREBASE_API_KEY"]


def register_user(email: str, password: str) -> dict:
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
    response = requests.post(
        url,
        json={"email": email, "password": password, "returnSecureToken": True},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
