import os
import firebase_admin
from firebase_admin import credentials
import requests


def initialize_firebase_admin():
    if not firebase_admin._apps:
        # GOOGLE_APPLICATION_CREDENTIALS environment variable must be set
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(
            cred,
            {
                "projectId": os.environ.get("FIREBASE_PROJECT_ID"),
            },
        )


def get_firebase_api_key():
    api_key = os.environ.get("FIREBASE_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_API_KEY environment variable not set.")
    return api_key


class FirebaseAuthClient:
    def __init__(self):
        self.api_key = get_firebase_api_key()
        self.identity_toolkit_base_url = "https://identitytoolkit.googleapis.com/v1"

    def sign_in_with_password(self, email, password):
        url = f"{self.identity_toolkit_base_url}/accounts:signInWithPassword?key={self.api_key}"
        payload = {"email": email, "password": password, "returnSecureToken": True}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def refresh_id_token(self, refresh_token):
        url = f"https://securetoken.googleapis.com/v1/token?key={self.api_key}"
        payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return {
            "id_token": data.get("id_token"),
            "refresh_token": data.get("refresh_token"),
            "expires_in": data.get("expires_in"),
            "local_id": data.get("user_id"),
        }


initialize_firebase_admin()
