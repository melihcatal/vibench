import requests
from identity_client import get_firebase_api_key
from identity_models import UserLoginRequest, UserLoginResponse

FIREBASE_AUTH_LOGIN_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key="

def email_password_login(request: UserLoginRequest) -> UserLoginResponse:
    api_key = get_firebase_api_key()
    url = f"{FIREBASE_AUTH_LOGIN_URL}{api_key}"
    payload = {
        "email": request.email,
        "password": request.password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    return UserLoginResponse(
        id_token=data["idToken"],
        refresh_token=data["refreshToken"],
        expires_in=int(data["expiresIn"])
    )
