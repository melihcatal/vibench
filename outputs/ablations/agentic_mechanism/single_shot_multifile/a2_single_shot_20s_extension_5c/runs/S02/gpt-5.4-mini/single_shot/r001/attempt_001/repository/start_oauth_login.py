import os
import secrets
import urllib.parse
from typing import Dict, Optional

import requests

from identity_client import get_identity_provider_config, store_pkce_state
from identity_models import OAuthLoginRequest, OAuthLoginResponse

AUTH0_AUTHORIZE_URL = "https://{domain}/authorize"


def build_oauth_login(request: Optional[OAuthLoginRequest] = None) -> OAuthLoginResponse:
    config = get_identity_provider_config()
    req = request or OAuthLoginRequest()
    state = req.state or secrets.token_urlsafe(32)
    nonce = req.nonce or secrets.token_urlsafe(24)
    code_verifier = req.code_verifier or secrets.token_urlsafe(64)
    code_challenge = req.code_challenge or code_verifier
    store_pkce_state(state=state, nonce=nonce, code_verifier=code_verifier)
    params: Dict[str, str] = {
        "client_id": config.client_id,
        "response_type": "code",
        "redirect_uri": req.redirect_uri or config.redirect_uri,
        "scope": req.scope or config.default_scope,
        "state": state,
        "nonce": nonce,
        "code_challenge": code_challenge,
        "code_challenge_method": req.code_challenge_method or "plain",
    }
    url = AUTH0_AUTHORIZE_URL.format(domain=config.provider_domain) + "?" + urllib.parse.urlencode(params)
    requests.utils.requote_uri(url)
    return OAuthLoginResponse(authorization_url=url, state=state, nonce=nonce)
