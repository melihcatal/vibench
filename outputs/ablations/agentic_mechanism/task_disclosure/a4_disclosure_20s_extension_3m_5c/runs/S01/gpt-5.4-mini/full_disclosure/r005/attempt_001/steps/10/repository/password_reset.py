import os
from typing import Any, Dict, Optional

import requests

AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CONNECTION_ENV = "AUTH0_CONNECTION"
AUTH0_PASSWORD_RESET_URL_PATH = "/dbconnections/change_password"


class PasswordResetError(RuntimeError):
    pass


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise PasswordResetError(f"Missing required environment variable: {name}")
    return value


def password_reset(email: str, *, client_id: Optional[str] = None, connection: Optional[str] = None, timeout: float = 30.0) -> Dict[str, Any]:
    domain = _require_env(AUTH0_DOMAIN_ENV).rstrip("/")
    payload: Dict[str, Any] = {
        "client_id": client_id or _require_env(AUTH0_CLIENT_ID_ENV),
        "email": email,
    }
    if connection is not None or os.getenv(AUTH0_CONNECTION_ENV):
        payload["connection"] = connection or _require_env(AUTH0_CONNECTION_ENV)
    url = f"https://{domain}{AUTH0_PASSWORD_RESET_URL_PATH}"
    response = requests.post(url, json=payload, timeout=timeout)
    try:
        data = response.json()
    except ValueError:
        data = {"raw": response.text}
    if response.status_code >= 400:
        message = data.get("error_description") or data.get("message") or data.get("raw") or "Auth0 password reset failed"
        raise PasswordResetError(message)
    return data


__all__ = ["password_reset", "PasswordResetError"]
