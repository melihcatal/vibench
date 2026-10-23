import base64
import json

import requests

from identity_client import load_identity_config
from identity_models import normalize_claims


def _decode_jwt_claims(token: str):
    payload = token.split(".")[1]
    padding = "=" * (-len(payload) % 4)
    return json.loads(base64.urlsafe_b64decode((payload + padding).encode()).decode())


def profile_claims(payload, config=None):
    config = config or load_identity_config()
    headers = {"Authorization": f"Bearer {payload['access_token']}"}
    if config.get("issuer"):
        response = requests.get(f"{config['issuer'].rstrip('/')}/oauth2/userInfo", headers=headers, timeout=30)
        response.raise_for_status()
        claims = response.json()
    else:
        claims = _decode_jwt_claims(payload.get("id_token", payload["access_token"]))
    return normalize_claims(claims)
