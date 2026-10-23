import os

import requests

from identity_client import auth0_issuer, json_headers, load_config
from identity_models import RegisterUserRequest, normalize_identity_request


def register_user(email: str, password: str, given_name: str = None):
    cfg = load_config()
    body = normalize_identity_request(
        {"email": email, "password": password, "given_name": given_name}
    )
    resp = requests.post(
        f"{auth0_issuer(cfg)}/dbconnections/signup",
        headers=json_headers(),
        json={
            "client_id": cfg.auth0_client_id,
            "email": body["email"],
            "password": body["password"],
            "connection": os.getenv(
                "AUTH0_CONNECTION", "Username-Password-Authentication"
            ),
            "user_metadata": {"given_name": body.get("given_name")}
            if body.get("given_name")
            else {},
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    raise SystemExit("import and call register_user()")


if __name__ == "__main__":
    main()
