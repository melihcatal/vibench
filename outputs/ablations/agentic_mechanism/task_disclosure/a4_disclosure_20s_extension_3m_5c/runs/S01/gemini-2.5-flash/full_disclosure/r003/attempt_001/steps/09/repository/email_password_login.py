import requests
import os

def sign_in_user(email: str, password: str) -> dict:
    """
    Signs in a user with email and password using Firebase Authentication REST API
    and returns ID and refresh tokens.
    """
    firebase_web_api_key = os.getenv("FIREBASE_WEB_API_KEY")
    if not firebase_web_api_key:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable not set.")

    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_web_api_key}"

    headers = {"Content-Type": "application/json"}
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    try:
        response = requests.post(rest_api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.HTTPError as err:
        error_message = err.response.json().get("error", {}).get("message", "Unknown error")
        raise ConnectionError(f"Firebase Authentication Error: {error_message}") from err
    except requests.exceptions.RequestException as err:
        raise ConnectionError(f"Network or request error: {err}") from err
