import requests
from identity_client import get_auth0_config, build_headers, build_base_url
from identity_models import PasswordResetRequest, normalize_email


def password_reset(email: str):
    cfg = get_auth0_config()
    payload = PasswordResetRequest(email=normalize_email(email), connection=cfg.connection).to_dict()
    url = f"{build_base_url(cfg)}/dbconnections/change_password"
    resp = requests.post(url, headers=build_headers(cfg), json=payload, timeout=30)
    resp.raise_for_status()
    return {"status": "requested", "result": resp.text}
