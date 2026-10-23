from __future__ import annotations

from identity_client import build_authorization_url, load_okta_config
from identity_models import OAuthStartRequest


def start_oauth_login(request: OAuthStartRequest) -> dict[str, str]:
    config = load_okta_config()
    params = {
        "client_id": config.client_id,
        "response_type": "code",
        **request.to_params(),
    }
    authorization_url = build_authorization_url(config.authorization_endpoint, params)
    return {
        "provider": "okta",
        "authorization_url": authorization_url,
        "issuer": config.issuer,
    }
