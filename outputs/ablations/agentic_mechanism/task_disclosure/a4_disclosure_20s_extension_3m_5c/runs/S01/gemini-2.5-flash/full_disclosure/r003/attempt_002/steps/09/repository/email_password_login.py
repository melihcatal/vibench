import os
import requests
import json

def sign_in_with_email_and_password(email, password):
    """
    Signs in a user with email and password using Firebase Authentication REST API
    and returns ID and refresh tokens.
    """
    # Firebase project configuration - these should ideally come from environment variables
    # or a secure configuration management system.
    FIREBASE_API_KEY = os.environ.get("FIREBASE_API_KEY")

    if not FIREBASE_API_KEY:
        raise ValueError("FIREBASE_API_KEY environment variable not set.")

    # Firebase Authentication endpoint for email/password sign-in
    FIREBASE_SIGN_IN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": True
    })

    try:
        response = requests.post(FIREBASE_SIGN_IN_URL, headers=headers, data=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        response_data = response.json()
        
        # Extract and return relevant tokens
        id_token = response_data.get("idToken")
        refresh_token = response_data.get("refreshToken")
        
        return {"idToken": id_token, "refreshToken": refresh_token}

    except requests.exceptions.HTTPError as e:
        error_message = e.response.json().get("error", {}).get("message", "Unknown error")
        raise Exception(f"Firebase sign-in failed: {error_message}") from e
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network or request error: {e}") from e
