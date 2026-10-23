import requests
from identity_client import FIREBASE_WEB_API_KEY
from identity_models import login_request

FIREBASE_AUTH_REST_API_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=" + FIREBASE_WEB_API_KEY

def email_password_login(email, password):
    """
    Signs in a user with email and password using Firebase Authentication REST API
    and returns authentication tokens.
    """
    payload = login_request(email, password)
    try:
        response = requests.post(FIREBASE_AUTH_REST_API_URL, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "message": "Failed to sign in."}
