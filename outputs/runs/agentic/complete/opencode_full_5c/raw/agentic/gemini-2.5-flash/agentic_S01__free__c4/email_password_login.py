import requests
from identity_models import LoginRequest, AuthResponse
from identity_client import get_firebase_web_api_key


def email_password_login(request: LoginRequest) -> AuthResponse:
    api_key = get_firebase_web_api_key()
    firebase_auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

    payload = {
        "email": request.email,
        "password": request.password,
        "returnSecureToken": True,
    }

    try:
        response = requests.post(firebase_auth_url, json=payload)
        response.raise_for_status()
        data = response.json()

        return AuthResponse(
            id_token=data["idToken"],
            refresh_token=data["refreshToken"],
            expires_in=data["expiresIn"],
            local_id=data["localId"],
        )
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Firebase login failed: {e}")
