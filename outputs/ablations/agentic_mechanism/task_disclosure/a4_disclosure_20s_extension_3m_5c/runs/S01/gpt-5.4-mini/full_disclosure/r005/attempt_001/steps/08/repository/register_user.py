import os
from typing import Any, Dict, Optional

import requests

AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_CONNECTION_ENV = "AUTH0_CONNECTION"
AUTH0_AUDIENCE_ENV = "AUTH0_AUDIENCE"
AUTH0_SIGNUP_URL_PATH = "/dbconnections/signup"


class RegisterUserError(RuntimeError):
    pass


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RegisterUserError(f"Missing required environment variable: {name}")
    return value


def register_user(email: str, password: str, *, user_metadata: Optional[Dict[str, Any]] = None, connection: Optional[str] = None, client_id: Optional[str] = None, client_secret: Optional[str] = None, audience: Optional[str] = None, timeout: float = 30.0) -> Dict[str, Any]:
    domain = _require_env(AUTH0_DOMAIN_ENV).rstrip("/")
    payload: Dict[str, Any] = {
        "client_id": client_id or _require_env(AUTH0_CLIENT_ID_ENV),
        "email": email,
        "password": password,
        "connection": connection or _require_env(AUTH0_CONNECTION_ENV),
    }
    if client_secret is not None or os.getenv(AUTH0_CLIENT_SECRET_ENV):
        payload["client_secret"] = client_secret or _require_env(AUTH0_CLIENT_SECRET_ENV)
    if audience is not None or os.getenv(AUTH0_AUDIENCE_ENV):
        payload["audience"] = audience or _require_env(AUTH0_AUDIENCE_ENV)
    if user_metadata:
        payload["user_metadata"] = user_metadata
    url = f"https://{domain}{AUTH0_SIGNUP_URL_PATH}"
    response = requests.post(url, json=payload, timeout=timeout)
    try:
        data = response.json()
    except ValueError:
        data = {"raw": response.text}
    if response.status_code >= 400:
        message = data.get("error_description") or data.get("message") or data.get("raw") or "Auth0 signup failed"
        raise RegisterUserError(message)
    return data


__all__ = ["register_user", "RegisterUserError"]
