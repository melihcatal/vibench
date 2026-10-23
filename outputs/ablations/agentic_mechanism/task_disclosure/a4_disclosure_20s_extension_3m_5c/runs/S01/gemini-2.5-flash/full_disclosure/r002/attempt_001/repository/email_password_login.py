import requests
import os

FIREBASE_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY", "YOUR_FIREBASE_WEB_API_KEY")

def email_password_login(email, password):
    """
    Signs in a user with email and password using Firebase Authentication and returns tokens.
    """
    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    try:
        response = requests.post(rest_api_url, headers=headers, json=payload)
        response.raise_for_status()
        user_data = response.json()

        id_token = user_data.get("idToken")
        refresh_token = user_data.get("refreshToken")

        if id_token and refresh_token:
            return {
                "id_token": id_token,
                "refresh_token": refresh_token,
                "expires_in": user_data.get("expiresIn"),
                "local_id": user_data.get("localId")
            }
        else:
            return {"error": "Failed to retrieve tokens from Firebase response."}

    except requests.exceptions.RequestException as e:
        return {"error": f"Firebase API request failed: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}
