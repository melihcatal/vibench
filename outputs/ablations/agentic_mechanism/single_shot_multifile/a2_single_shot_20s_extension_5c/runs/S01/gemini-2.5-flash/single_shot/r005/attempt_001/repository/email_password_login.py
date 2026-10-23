import requests
from identity_client import config
from identity_models import LoginRequest, LoginResponse

FIREBASE_SIGN_IN_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

def email_password_login(request: LoginRequest) -> LoginResponse:
    """
    Signs in a user with email and password using Firebase Authentication REST API
    and returns ID and refresh tokens.
    """
    payload = {
        "email": request.email,
        "password": request.password,
        "returnSecureToken": True
    }
    params = {"key": config.firebase_api_key}

    try:
        response = requests.post(FIREBASE_SIGN_IN_URL, json=payload, params=params)
        response.raise_for_status()
        data = response.json()

        return LoginResponse(
            id_token=data["idToken"],
            refresh_token=data["refreshToken"],
            expires_in=data["expiresIn"]
        )
    except requests.exceptions.HTTPError as e:
        error_data = e.response.json()
        error_message = error_data.get("error", {}).get("message", "Unknown error")
        raise RuntimeError(f"Failed to log in: {error_message} (HTTP Status: {e.response.status_code})")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during login: {e}")
