import json
from typing import Dict

import requests

from identity_client import microsoft_token_url, token_payload
from identity_models import OAuthTokens


def exchange_code_for_tokens(code: str, redirect_uri: str, code_verifier: str) -> OAuthTokens:
    response = requests.post(microsoft_token_url(), data=token_payload(code, redirect_uri, code_verifier), timeout=30)
    response.raise_for_status()
    data: Dict[str, str] = response.json()
    return OAuthTokens(
        access_token=data["access_token"],
        id_token=data.get("id_token"),
        refresh_token=data.get("refresh_token"),
        token_type=data.get("token_type", "Bearer"),
        expires_in=data.get("expires_in"),
        raw=json.loads(json.dumps(data)),
    )
