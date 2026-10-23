import os
import requests
from identity_models import (
    RegisterUserRequest,
    RegisterUserResponse,
    normalize_register_request,
    parse_register_response,
)

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET", "")
AUTH0_MANAGEMENT_API_AUDIENCE = os.environ.get("AUTH0_MANAGEMENT_API_AUDIENCE", "")


def _get_management_token():
    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "audience": AUTH0_MANAGEMENT_API_AUDIENCE,
        "grant_type": "client_credentials",
    }
    resp = requests.post(url, json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()["access_token"]


def register_user(request: RegisterUserRequest) -> RegisterUserResponse:
    token = _get_management_token()
    normalized = normalize_register_request(request)
    url = f"https://{AUTH0_DOMAIN}/api/v2/users"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    body = {
        "email": normalized.email,
        "password": normalized.password,
        "connection": normalized.connection,
        "user_metadata": normalized.user_metadata or {},
        "app_metadata": normalized.app_metadata or {},
    }
    resp = requests.post(url, json=body, headers=headers, timeout=15)
    resp.raise_for_status()
    return parse_register_response(resp.json())
