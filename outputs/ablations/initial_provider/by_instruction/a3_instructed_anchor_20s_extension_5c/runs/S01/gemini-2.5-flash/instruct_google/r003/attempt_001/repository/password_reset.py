import requests
import os

class PasswordResetRequest:
    def __init__(self, email: str):
        self.email = email

class PasswordResetResponse:
    def __init__(self, email: str):
        self.email = email

def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    api_key = os.environ.get("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable not set.")

    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={api_key}"

    headers = {"Content-Type": "application/json"}
    payload = {
        "requestType": "PASSWORD_RESET",
        "email": request.email
    }

    try:
        response = requests.post(rest_api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        return PasswordResetResponse(email=data.get("email"))
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error during password reset: {e.response.text}")
        raise
    except Exception as e:
        print(f"Error during password reset: {e}")
        raise
