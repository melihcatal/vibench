import os
import secrets
from urllib.parse import urlencode

import requests

from identity_client import build_oidc_config, build_state_payload, redirect_uri_for

PROVIDER_HOST = os.environ.get("IDP_PROVIDER_HOST", "https://login.microsoftonline.com")
AUTHORIZE_PATH = os.environ.get("IDP_AUTHORIZE_PATH", "/common/oauth2/v2.0/authorize")
CLIENT_ID = os.environ.get("IDP_CLIENT_ID", "")
SCOPES = os.environ.get("IDP_SCOPES", "openid profile email offline_access")
RESPONSE_TYPE = "code"
RESPONSE_MODE = "query"


def start_login(redirect_uri: str | None = None, nonce: str | None = None, code_challenge: str | None = None) -> dict:
    cfg = build_oidc_config()
    redirect = redirect_uri or redirect_uri_for(cfg)
    state = build_state_payload({"nonce": nonce or secrets.token_urlsafe(16), "flow": "oauth"})
    params = {
        "client_id": CLIENT_ID or cfg.client_id,
        "response_type": RESPONSE_TYPE,
        "response_mode": RESPONSE_MODE,
        "redirect_uri": redirect,
        "scope": SCOPES,
        "state": state,
    }
    if nonce:
        params["nonce"] = nonce
    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = "S256"
    url = f"{PROVIDER_HOST.rstrip('/')}{AUTHORIZE_PATH}"
    return {"authorization_url": f"{url}?{urlencode(params)}", "state": state, "redirect_uri": redirect}


def exchange_preview() -> dict:
    cfg = build_oidc_config()
    well_known = cfg.discovery_url()
    response = requests.get(well_known, timeout=10)
    response.raise_for_status()
    return response.json()
