import os
import requests
from identity_models import EmailPasswordLoginRequest, EmailPasswordLoginResponse

FIREBASE_WEB_API_KEY = os.getenv("FIREBASE_WEB_API_KEY")


def email_password_login(
    request: EmailPasswordLoginRequest,
) -> EmailPasswordLoginResponse:
    if not FIREBASE_WEB_API_KEY:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable is not set.")

    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "email": request.email,
        "password": request.password,
        "returnSecureToken": True,
    }

    try:
        response = requests.post(rest_api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_data = response.json()
        return EmailPasswordLoginResponse(
            idToken=response_data["idToken"],
            refreshToken=response_data["refreshToken"],
            expiresIn=response_data["expiresIn"],
        )
    except requests.exceptions.RequestException as e:
        # In a real application, parse Firebase error response for more details
        error_message = response.json().get("error", {}).get("message", str(e))
        raise RuntimeError(f"Failed to login user: {error_message}")
