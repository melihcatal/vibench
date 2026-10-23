import base64
import json
import urllib.error
import urllib.parse
import urllib.request

from identity_client import build_basic_auth_header, load_identity_config
from identity_models import TokenResponse


def exchange_code_for_tokens(code: str) -> TokenResponse:
    cfg = load_identity_config()
    payload = urllib.parse.urlencode(
        {
            "grant_type": "authorization_code",
            "client_id": cfg.client_id,
            "code": code,
            "redirect_uri": cfg.redirect_uri,
        }
    ).encode()
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    headers.update(build_basic_auth_header(cfg.client_id, cfg.client_secret))
    req = urllib.request.Request(cfg.token_url, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode())
    return TokenResponse(
        access_token=data["access_token"],
        id_token=data.get("id_token"),
        refresh_token=data.get("refresh_token"),
        token_type=data.get("token_type", "Bearer"),
        expires_in=data.get("expires_in"),
    )
