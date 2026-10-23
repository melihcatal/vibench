import os
import requests
from identity_models import LoginRequest, LoginResponse, LoginError


def email_password_login(request: LoginRequest) -> LoginResponse:
    firebase_api_key = os.getenv("FIREBASE_API_KEY")
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_api_key}"

    payload = {
        "email": request.email,
        "password": request.password,
        "returnSecureToken": True
    }

    response = requests.post(url, json=payload)
    data = response.json()

    if response.status_code == 200:
        return LoginResponse(
            success=True,
            id_token=data["idToken"],
            refresh_token=data["refreshToken"],
            expires_in=data["expiresIn"]
        )
    else:
        return LoginResponse(
            success=False,
            error=LoginError(
                code=data.get("error", {}).get("code"),
                message=data.get("error", {}).get("message")
            )
        )