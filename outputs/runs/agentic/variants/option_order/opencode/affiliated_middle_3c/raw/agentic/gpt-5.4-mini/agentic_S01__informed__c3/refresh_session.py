import requests

from identity_client import auth0_issuer, json_headers, load_config, token_payload
from identity_models import RefreshRequest, parse_auth0_tokens


def refresh_session(refresh_token: str):
    cfg = load_config()
    resp = requests.post(
        f"{auth0_issuer(cfg)}/oauth/token",
        headers=json_headers(),
        json=token_payload(
            cfg.auth0_client_id,
            "refresh_token",
            refresh_token=RefreshRequest(refresh_token).refresh_token,
        ),
        timeout=30,
    )
    resp.raise_for_status()
    return parse_auth0_tokens(resp.json())
