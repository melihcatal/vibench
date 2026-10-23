import requests
from identity_models import LoginRequest, LoginResponse
import os


def email_password_login(request: LoginRequest) -> LoginResponse:
    auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={os.getenv('FIREBASE_API_KEY')}"
    payload = {
        "email": request.email,
        "password": request.password,
        "returnSecureToken": True,
    }
    response = requests.post(auth_url, json=payload)

    if response.status_code == 200:
        data = response.json()
        return LoginResponse(
            success=True,
            id_token=data["idToken"],
            refresh_token=data["refreshToken"],
            expires_in=data["expiresIn"],
        )
    else:
        return LoginResponse(
            success=False,
            error=response.json().get("error", {}).get("message", "Login failed"),
        )
