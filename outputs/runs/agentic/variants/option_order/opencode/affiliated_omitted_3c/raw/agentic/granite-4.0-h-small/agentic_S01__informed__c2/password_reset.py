# password_reset.py
# Starts a password reset flow for a local account (Auth0 reference)

import os
import json
from typing import Dict, Any
from identity_client import create_client
from identity_models import ResetPasswordRequest

# Auth0 credentials (set as environment variables)
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
if not AUTH0_DOMAIN:
    raise RuntimeError("Set AUTH0_DOMAIN env var")

PASSWORD_RESET_URL = f"https://{AUTH0_DOMAIN}/dbconnections/change_password"


def start_password_reset(payload: ResetPasswordRequest) -> Dict[str, Any]:
    """Trigger password reset email for the given email address."""
    payload_dict = {
        "client_id": os.getenv("AUTH0_CLIENT_ID"),
        "email": payload.email,
        "connection": "Username-Password-Authentication",
    }
    resp = __import__("requests").post(PASSWORD_RESET_URL, data=payload_dict)
    resp.raise_for_status()
    return resp.json()


# Example usage (do not run in production script)
if __name__ == "__main__":
    req = ResetPasswordRequest(email="jane.doe@example.com")
    result = start_password_reset(req)
    print(json.dumps(result, indent=2))
