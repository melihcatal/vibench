import os
import requests
from identity_models import (
    LoginRequest,
    LoginResponse,
    normalize_login_request,
    parse_login_response,
)

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")


def email_password_login(request: LoginRequest) -> LoginResponse:
    normalized = normalize_login_request(request)
    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "password",
        "username": normalized.email,
        "password": normalized.password,
        "client_id": AUTH0_CLIENT_ID,
        "audience": os.environ.get("AUTH0_API_AUDIENCE", ""),
        "scope": normalized.scope or "openid profile email offline_access",
    }
    resp = requests.post(url, json=payload, timeout=15)
    resp.raise_for_status()
    return parse_login_response(resp.json())
