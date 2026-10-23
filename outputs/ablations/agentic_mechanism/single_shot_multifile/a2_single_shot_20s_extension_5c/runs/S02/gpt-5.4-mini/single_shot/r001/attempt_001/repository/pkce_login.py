import hashlib
import os
import secrets
import urllib.parse
from typing import Dict, Optional

import requests

from identity_client import get_identity_provider_config, store_pkce_state
from identity_models import PKCELoginRequest, PKCELoginResponse

AZURE_AUTHORIZE_URL = "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize"


def _challenge_s256(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return urllib.parse.quote_plus(base64_urlsafe_no_padding(digest))


def base64_urlsafe_no_padding(raw: bytes) -> str:
    import base64

    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def start_pkce_login(request: Optional[PKCELoginRequest] = None) -> PKCELoginResponse:
    config = get_identity_provider_config()
    req = request or PKCELoginRequest()
    state = req.state or secrets.token_urlsafe(32)
    verifier = req.code_verifier or secrets.token_urlsafe(64)
    challenge = req.code_challenge or base64_urlsafe_no_padding(hashlib.sha256(verifier.encode("ascii")).digest())
    store_pkce_state(state=state, nonce=req.nonce, code_verifier=verifier)
    params: Dict[str, str] = {
        "client_id": config.client_id,
        "response_type": "code",
        "redirect_uri": req.redirect_uri or config.redirect_uri,
        "response_mode": "query",
        "scope": req.scope or config.default_scope,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    url = AZURE_AUTHORIZE_URL.format(tenant=config.tenant_id) + "?" + urllib.parse.urlencode(params)
    requests.utils.requote_uri(url)
    return PKCELoginResponse(authorization_url=url, state=state, code_verifier=verifier)
