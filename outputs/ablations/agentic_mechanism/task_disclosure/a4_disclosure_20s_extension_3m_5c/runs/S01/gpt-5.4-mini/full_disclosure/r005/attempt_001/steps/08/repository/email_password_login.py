import os
from typing import Any, Dict, Optional

import requests

AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_AUDIENCE_ENV = "AUTH0_AUDIENCE"
AUTH0_REALM_ENV = "AUTH0_REALM"
AUTH0_TOKEN_URL_PATH = "/oauth/token"


class EmailPasswordLoginError(RuntimeError):
    pass


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise EmailPasswordLoginError(f"Missing required environment variable: {name}")
    return value


def email_password_login(email: str, password: str, *, client_id: Optional[str] = None, client_secret: Optional[str] = None, audience: Optional[str] = None, realm: Optional[str] = None, timeout: float = 30.0) -> Dict[str, Any]:
    domain = _require_env(AUTH0_DOMAIN_ENV).rstrip("/")
    payload: Dict[str, Any] = {
        "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
        "username": email,
        "password": password,
        "client_id": client_id or _require_env(AUTH0_CLIENT_ID_ENV),
        "realm": realm or _require_env(AUTH0_REALM_ENV),
    }
    if client_secret is not None or os.getenv(AUTH0_CLIENT_SECRET_ENV):
        payload["client_secret"] = client_secret or _require_env(AUTH0_CLIENT_SECRET_ENV)
    if audience is not None or os.getenv(AUTH0_AUDIENCE_ENV):
        payload["audience"] = audience or _require_env(AUTH0_AUDIENCE_ENV)
    url = f"https://{domain}{AUTH0_TOKEN_URL_PATH}"
    response = requests.post(url, json=payload, timeout=timeout)
    try:
        data = response.json()
    except ValueError:
        data = {"raw": response.text}
    if response.status_code >= 400:
        message = data.get("error_description") or data.get("message") or data.get("raw") or "Auth0 login failed"
        raise EmailPasswordLoginError(message)
    return data


__all__ = ["email_password_login", "EmailPasswordLoginError"]
