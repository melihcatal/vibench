import os
import requests
from identity_models import LoginRequest, LoginResponse

def email_password_login(email: str, password: str) -> LoginResponse:
    domain = os.getenv("AUTH0_DOMAIN")
    client_id = os.getenv("AUTH0_CLIENT_ID")
    client_secret = os.getenv("AUTH0_CLIENT_SECRET")
    
    token_url = f"https://{domain}/oauth/token"
    payload = {
        "grant_type": "password",
        "username": email,
        "password": password,
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": f"https://{domain}/api/v2/",
        "scope": "openid profile email"
    }
    
    response = requests.post(token_url, json=payload)
    response.raise_for_status()
    token_data = response.json()
    
    return LoginResponse(
        access_token=token_data["access_token"],
        id_token=token_data["id_token"],
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data["expires_in"]
    )