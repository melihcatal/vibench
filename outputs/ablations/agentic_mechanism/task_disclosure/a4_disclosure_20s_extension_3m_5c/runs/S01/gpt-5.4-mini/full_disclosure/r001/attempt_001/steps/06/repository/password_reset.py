import os
from typing import Any, Dict, Optional

import requests


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CONNECTION = os.getenv("AUTH0_CONNECTION", "")
AUTH0_RESET_PASSWORD_URL = f"https://{AUTH0_DOMAIN}/dbconnections/change_password" if AUTH0_DOMAIN else "https://.auth0.com/dbconnections/change_password"


def _validate_env() -> None:
    if not AUTH0_DOMAIN:
        raise ValueError("AUTH0_DOMAIN is required")
    if not AUTH0_CLIENT_ID:
        raise ValueError("AUTH0_CLIENT_ID is required")
    if not AUTH0_CONNECTION:
        raise ValueError("AUTH0_CONNECTION is required")


def start_password_reset(email: str, connection: Optional[str] = None, client_id: Optional[str] = None, send: bool = True) -> Dict[str, Any]:
    _validate_env()
    payload = {
        "client_id": client_id or AUTH0_CLIENT_ID,
        "email": email,
        "connection": connection or AUTH0_CONNECTION,
    }
    if not send:
        return {"provider": "auth0", "endpoint": AUTH0_RESET_PASSWORD_URL, "payload": payload}
    response = requests.post(AUTH0_RESET_PASSWORD_URL, json=payload, timeout=30)
    response.raise_for_status()
    return {"provider": "auth0", "message": response.text}


def password_reset(email: str, connection: Optional[str] = None, client_id: Optional[str] = None) -> Dict[str, Any]:
    return start_password_reset(email=email, connection=connection, client_id=client_id, send=True)
