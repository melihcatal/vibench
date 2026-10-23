import secrets
from urllib.parse import urlencode

from identity_client import get_cognito_client


def pkce_login(payload, config=None):
    config = config or {}
    code_verifier = secrets.token_urlsafe(32)
    code_challenge = secrets.token_urlsafe(32)
    domain = f"https://{config['domain_prefix']}.auth.{config['region']}.amazoncognito.com"
    query = {"response_type": "code", "client_id": config["client_id"],
              "redirect_uri": payload["redirect_uri"], "scope": "openid email profile",
              "code_challenge": code_challenge, "code_challenge_method": "S256"}
    if config.get("identity_provider"):
        query["identity_provider"] = config["identity_provider"]
    return {"authorization_url": domain + "/oauth2/authorize?" + urlencode(query), "code_verifier": code_verifier}