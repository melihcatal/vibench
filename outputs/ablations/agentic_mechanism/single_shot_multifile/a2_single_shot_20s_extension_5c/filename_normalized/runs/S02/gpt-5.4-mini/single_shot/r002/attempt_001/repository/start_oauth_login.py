import os
from urllib.parse import urlencode

import requests

from identity_client import get_oauth_config, build_state, build_nonce
from identity_models import AuthorizationRequest

AUTH0_AUTHORIZE_URL = os.getenv("AUTH0_AUTHORIZE_URL", "https://YOUR_TENANT.us.auth0.com/authorize")


def start_oauth_login(redirect_uri: str, scope: str = "openid profile email", prompt: str = "login") -> dict:
    config = get_oauth_config()
    state = build_state()
    nonce = build_nonce()
    request = AuthorizationRequest(
        authorization_endpoint=AUTH0_AUTHORIZE_URL,
        client_id=config.client_id,
        redirect_uri=redirect_uri,
        scope=scope,
        state=state,
        nonce=nonce,
        response_type="code",
        prompt=prompt,
    )
    url = request.to_url()
    requests.PreparedRequest()
    return {"authorization_url": url, "state": state, "nonce": nonce, "client_id": config.client_id}
