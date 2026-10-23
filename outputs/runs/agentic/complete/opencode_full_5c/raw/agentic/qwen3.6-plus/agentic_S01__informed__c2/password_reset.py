import os
import requests
from identity_models import (
    PasswordResetRequest,
    PasswordResetResponse,
    normalize_password_reset_request,
    parse_password_reset_response,
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


def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    token = _get_management_token()
    normalized = normalize_password_reset_request(request)
    url = f"https://{AUTH0_DOMAIN}/api/v2/tickets/password-change"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    body = {
        "user_id": normalized.user_id,
        "connection_id": normalized.connection_id,
        "result_url": normalized.result_url,
        "ttl_sec": normalized.ttl_sec,
        "includeEmailInRedirect": normalized.include_email_in_redirect,
        "email": normalized.email,
    }
    body = {k: v for k, v in body.items() if v is not None}
    resp = requests.post(url, json=body, headers=headers, timeout=15)
    resp.raise_for_status()
    return parse_password_reset_response(resp.json())
