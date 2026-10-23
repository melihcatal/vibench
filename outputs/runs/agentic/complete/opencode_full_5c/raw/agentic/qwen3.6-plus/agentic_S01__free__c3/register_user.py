import os
import httpx
from identity_models import (
    RegisterRequest,
    RegisterResponse,
    normalize_register_response,
)


AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "dev-example.us.auth0.com")
AUTH0_MANAGEMENT_API_AUDIENCE = "https://{}/api/v2/".format(AUTH0_DOMAIN)
AUTH0_MANAGEMENT_API_TOKEN = os.environ.get("AUTH0_MANAGEMENT_API_TOKEN", "")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET", "")


def get_management_token():
    if AUTH0_MANAGEMENT_API_TOKEN:
        return AUTH0_MANAGEMENT_API_TOKEN
    token_url = "https://{}/oauth/token".format(AUTH0_DOMAIN)
    payload = {
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "audience": AUTH0_MANAGEMENT_API_AUDIENCE,
        "grant_type": "client_credentials",
    }
    resp = httpx.post(token_url, json=payload)
    resp.raise_for_status()
    return resp.json()["access_token"]


def register_user(
    email, password, connection="Username-Password-Authentication", metadata=None
):
    req = RegisterRequest(
        email=email, password=password, connection=connection, metadata=metadata or {}
    )
    token = get_management_token()
    url = "https://{}/api/v2/users".format(AUTH0_DOMAIN)
    headers = {
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json",
    }
    body = {
        "email": req.email,
        "password": req.password,
        "connection": req.connection,
        "user_metadata": req.metadata,
    }
    resp = httpx.post(url, json=body, headers=headers)
    resp.raise_for_status()
    return normalize_register_response(resp.json())
