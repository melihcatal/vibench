import os
import requests

def email_password_login(email: str, password: str):
    """
    Signs in a user with email and password using Firebase Authentication REST API
    and returns ID and refresh tokens.
    """
    firebase_api_key = os.environ.get("FIREBASE_API_KEY")
    if not firebase_api_key:
        raise ValueError("FIREBASE_API_KEY environment variable not set.")

    rest_api_endpoint = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_api_key}"

    headers = {"Content-Type": "application/json"}
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    try:
        response = requests.post(rest_api_endpoint, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return {
            "idToken": data.get("idToken"),
            "refreshToken": data.get("refreshToken"),
            "expiresIn": data.get("expiresIn"),
            "localId": data.get("localId")
        }
    except requests.exceptions.RequestException as e:
        error_message = f"Firebase authentication failed: {e}"
        if response.content:
            try:
                error_data = response.json()
                error_message += f" - {error_data.get('error', {}).get('message', 'Unknown error')}"
            except ValueError:
                error_message += f" - Raw response: {response.text}"
        raise RuntimeError(error_message)

