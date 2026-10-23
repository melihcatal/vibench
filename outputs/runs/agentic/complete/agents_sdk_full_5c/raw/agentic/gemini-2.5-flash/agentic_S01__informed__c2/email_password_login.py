import requests
from identity_client import get_firebase_web_api_key
from identity_models import EmailPasswordLoginRequest, EmailPasswordLoginResponse

FIREBASE_AUTH_REST_API = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

def email_password_login(request: EmailPasswordLoginRequest) -> EmailPasswordLoginResponse:
    api_key = get_firebase_web_api_key()
    payload = {
        "email": request['email'],
        "password": request['password'],
        "returnSecureToken": True
    }
    try:
        response = requests.post(f"{FIREBASE_AUTH_REST_API}?key={api_key}", json=payload)
        response.raise_for_status()
        data = response.json()
        return {
            "id_token": data['idToken'],
            "refresh_token": data['refreshToken'],
            "expires_in": data['expiresIn']
        }
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to login user: {e}, Response: {getattr(e.response, 'text', 'No response text')}")

