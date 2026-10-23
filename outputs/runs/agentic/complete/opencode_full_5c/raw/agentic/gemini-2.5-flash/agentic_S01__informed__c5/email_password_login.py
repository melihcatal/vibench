import os
import requests
from identity_models import LoginRequest, LoginResponse


def email_password_login(request: LoginRequest) -> LoginResponse:
    url = f"https://{os.environ.get('AUTH0_DOMAIN')}/oauth/token"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": request.grant_type,
        "username": request.username,
        "password": request.password,
        "audience": request.audience,
        "scope": request.scope,
        "client_id": request.client_id,
        "client_secret": request.client_secret,
    }
    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()
    return LoginResponse(**response.json())
