import os
import requests

def register_user(email, password):
    """
    Registers a new user with email and password using Google Firebase Authentication.
    """
    api_key = os.environ.get("FIREBASE_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_API_KEY environment variable not set.")

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error registering user: {e}")
        if response and response.content:
            print(f"Response content: {response.content.decode()}")
        raise
