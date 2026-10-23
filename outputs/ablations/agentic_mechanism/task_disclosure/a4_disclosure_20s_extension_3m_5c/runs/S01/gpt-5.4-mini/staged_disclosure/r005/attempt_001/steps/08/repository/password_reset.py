import os
from typing import Any, Dict

import requests


AUTH0_DOMAIN = os.environ["AUTH0_DOMAIN"]
AUTH0_CLIENT_ID = os.environ["AUTH0_CLIENT_ID"]


def start_password_reset(email: str) -> Dict[str, Any]:
    response = requests.post(
        f"https://{AUTH0_DOMAIN}/dbconnections/change_password",
        json={
            "client_id": AUTH0_CLIENT_ID,
            "email": email,
            "connection": os.environ.get("AUTH0_CONNECTION", "Username-Password-Authentication"),
        },
        timeout=30,
    )
    response.raise_for_status()
    return {"message": response.text}
