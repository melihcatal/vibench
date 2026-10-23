import requests
from identity_client import load_identity_config
from identity_models import EmailPasswordRequest, TokenResponse, as_payload, normalize_email


def email_password_login(email: str, password: str) -> dict:
    config = load_identity_config()
    req = EmailPasswordRequest(email=normalize_email(email), password=password)
    payload = as_payload(req)
    payload.update({
        "grant_type": "password",
        "username": req.email,
        "password": req.password,
        "audience": config.auth0_audience,
        "client_id": config.auth0_client_id,
        "client_secret": config.auth0_client_secret,
        "scope": "openid profile email offline_access",
        "realm": config.auth0_connection,
    })
    response = requests.post(f"https://{config.auth0_domain}/oauth/token", json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return as_payload(TokenResponse(access_token=data["access_token"], id_token=data.get("id_token"), refresh_token=data.get("refresh_token"), token_type=data.get("token_type", "Bearer"), expires_in=data.get("expires_in")))
