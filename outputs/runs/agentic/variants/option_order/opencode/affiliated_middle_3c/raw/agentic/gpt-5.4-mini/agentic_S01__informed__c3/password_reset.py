import requests

from identity_client import auth0_issuer, json_headers, load_config
from identity_models import PasswordResetRequest, normalize_identity_request


def password_reset(email: str):
    cfg = load_config()
    body = normalize_identity_request({"email": email})
    resp = requests.post(
        f"{auth0_issuer(cfg)}/dbconnections/change_password",
        headers=json_headers(),
        json={
            "client_id": cfg.auth0_client_id,
            "email": PasswordResetRequest(body["email"]).email,
            "connection": __import__("os").getenv(
                "AUTH0_CONNECTION", "Username-Password-Authentication"
            ),
        },
        timeout=30,
    )
    resp.raise_for_status()
    return {"status": "sent", "message": resp.text}
