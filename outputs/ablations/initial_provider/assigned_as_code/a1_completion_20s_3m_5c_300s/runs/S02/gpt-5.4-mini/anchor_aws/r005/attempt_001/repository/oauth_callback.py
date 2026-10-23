import requests

from identity_client import get_cognito_base_url, get_oauth_config
from identity_models import OAuthCallbackRequest, TokenResponse


def oauth_callback(payload, config=None):
    cfg = get_oauth_config(config)
    req = OAuthCallbackRequest.from_payload(payload)
    token_url = get_cognito_base_url(cfg) + "/oauth2/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": cfg.client_id,
        "code": req.code,
        "redirect_uri": req.redirect_uri,
    }
    if cfg.client_secret:
        data["client_secret"] = cfg.client_secret
    if req.code_verifier:
        data["code_verifier"] = req.code_verifier
    response = requests.post(token_url, data=data, timeout=30)
    response.raise_for_status()
    return TokenResponse.from_dict(response.json()).to_dict()
