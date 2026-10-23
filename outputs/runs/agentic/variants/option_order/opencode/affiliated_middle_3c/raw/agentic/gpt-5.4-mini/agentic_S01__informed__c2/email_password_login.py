import requests
from identity_client import get_auth0_config, build_headers, build_base_url
from identity_models import LoginRequest, TokenResponse, normalize_email


def email_password_login(email: str, password: str):
    cfg = get_auth0_config()
    payload = LoginRequest(email=normalize_email(email), password=password).to_dict()
    payload.update({"grant_type": "password", "audience": cfg.audience, "scope": cfg.scope, "realm": cfg.connection, "client_id": cfg.client_id, "client_secret": cfg.client_secret})
    url = f"{build_base_url(cfg)}/oauth/token"
    resp = requests.post(url, headers=build_headers(cfg), json=payload, timeout=30)
    resp.raise_for_status()
    return TokenResponse.from_dict(resp.json()).to_dict()
