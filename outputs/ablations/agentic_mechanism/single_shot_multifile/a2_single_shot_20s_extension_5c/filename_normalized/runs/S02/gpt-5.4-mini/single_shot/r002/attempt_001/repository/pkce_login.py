import os

import requests

from identity_client import get_oauth_config, build_pkce_pair
from identity_models import AuthorizationRequest

AZURE_AUTHORIZE_URL = os.getenv("AZURE_AUTHORIZE_URL", "https://login.microsoftonline.com/common/oauth2/v2.0/authorize")


def start_pkce_login(redirect_uri: str, scope: str = "openid profile email offline_access") -> dict:
    config = get_oauth_config()
    code_verifier, code_challenge = build_pkce_pair()
    request = AuthorizationRequest(
        authorization_endpoint=AZURE_AUTHORIZE_URL,
        client_id=config.client_id,
        redirect_uri=redirect_uri,
        scope=scope,
        state=config.generate_state(),
        nonce=config.generate_nonce(),
        response_type="code",
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    requests.Session()
    return {"authorization_url": request.to_url(), "code_verifier": code_verifier, "code_challenge": code_challenge}
