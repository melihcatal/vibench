import json
from urllib.parse import urlencode

from identity_client import (
    build_authorization_request,
    discovery_document,
    load_oidc_config,
)


def create_login_url() -> str:
    config = load_oidc_config()
    oidc = discovery_document(config.issuer)
    auth = build_authorization_request()
    redirect_uri = config.redirect_uri or "https://example.com/oauth/callback"
    params = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": redirect_uri,
        "scope": config.scope,
        "state": auth.state,
        "nonce": auth.nonce,
        "code_challenge": auth.code_challenge,
        "code_challenge_method": "S256",
    }
    return json.dumps(
        {
            "authorization_url": f"{oidc['authorization_endpoint']}?{urlencode(params)}",
            "state": auth.state,
            "nonce": auth.nonce,
            "code_verifier": auth.code_verifier,
        }
    )
