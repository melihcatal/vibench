import os
import requests
from identity_models import LoginUserRequest, LoginUserResponse

# Firebase Web API Key for client-side authentication.
# This would typically be stored securely, e.g., in environment variables.
FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")
FIREBASE_AUTH_REST_API = "https://identitytoolkit.googleapis.com/v1/accounts"

def email_password_login(request: LoginUserRequest) -> LoginUserResponse:
    if not FIREBASE_WEB_API_KEY:
        raise ValueError("FIREBASE_WEB_API_KEY not set.")

    url = f"{FIREBASE_AUTH_REST_API}:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    payload = {
        "email": request.email,
        "password": request.password,
        "returnSecureToken": True
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        data = response.json()

        return LoginUserResponse(
            id_token=data.get("idToken"),
            refresh_token=data.get("refreshToken"),
            expires_in=data.get("expiresIn"),
            local_id=data.get("localId"),
            email=data.get("email")
        )
    except requests.exceptions.HTTPError as e:
        error_data = e.response.json()
        error_message = error_data.get("error", {}).get("message", "Unknown error")
        raise RuntimeError(f"Firebase login failed: {error_message} (Status: {e.response.status_code})")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during login: {e}")
