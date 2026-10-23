import requests
from identity_client import get_auth0_config, build_headers, build_base_url
from identity_models import RefreshRequest, TokenResponse


def refresh_session(refresh_token: str):
    cfg = get_auth0_config()
    payload = RefreshRequest(refresh_token=refresh_token).to_dict()
    payload.update({"grant_type": "refresh_token", "client_id": cfg.client_id, "client_secret": cfg.client_secret})
    url = f"{build_base_url(cfg)}/oauth/token"
    resp = requests.post(url, headers=build_headers(cfg), json=payload, timeout=30)
    resp.raise_for_status()
    return TokenResponse.from_dict(resp.json()).to_dict()
