import requests

from identity_client import load_identity_config, merge_payload
from identity_models import build_token_payload


def oauth_callback(payload, config=None):
    cfg = load_identity_config(config)
    merged = merge_payload(payload, cfg)
    token_payload = build_token_payload(
        merged["code"],
        merged["redirect_uri"],
        merged.get("client_id"),
        merged.get("client_secret"),
        merged.get("code_verifier"),
    )
    response = requests.post(
        "https://oauth2.googleapis.com/token",
        data=token_payload,
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()
    return {"access_token": result.get("access_token"), "id_token": result.get("id_token"), "refresh_token": result.get("refresh_token"), "expires_in": result.get("expires_in")}
