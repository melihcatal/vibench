import os
import requests
from identity_models import LoginRequest, LoginResponse


def email_password_login(email: str, password: str) -> LoginResponse:
    auth0_domain = os.getenv("AUTH0_DOMAIN")
    client_id = os.getenv("AUTH0_CLIENT_ID")
    token_url = f"https://{auth0_domain}/oauth/token"

    request = LoginRequest(email=email, password=password, client_id=client_id)
    payload = {
        "grant_type": request.grant_type,
        "username": request.email,
        "password": password,
        "client_id": request.client_id,
    }
    response = requests.post(token_url, json=payload)
    response.raise_for_status()
    data = response.json()
    return LoginResponse(
        access_token=data["access_token"],
        refresh_token=data["refresh_token"],
        id_token=data["id_token"],
        expires_in=data["expires_in"],
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 3:
        email, password = sys.argv[1], sys.argv[2]
        response = email_password_login(email, password)
        print(f"Access Token: {response.access_token}")
