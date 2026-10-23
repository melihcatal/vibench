import requests

from identity_client import auth0_issuer, json_headers, load_config, token_payload
from identity_models import LoginRequest, normalize_identity_request, parse_auth0_tokens


def email_password_login(email: str, password: str):
    cfg = load_config()
    body = normalize_identity_request({"email": email, "password": password})
    resp = requests.post(
        f"{auth0_issuer(cfg)}/oauth/token",
        headers=json_headers(),
        json=token_payload(
            cfg.auth0_client_id,
            "password",
            username=body["email"],
            password=body["password"],
            audience=cfg.auth0_audience,
            scope="openid profile email offline_access",
            realm="Username-Password-Authentication",
        ),
        timeout=30,
    )
    resp.raise_for_status()
    return parse_auth0_tokens(resp.json())
