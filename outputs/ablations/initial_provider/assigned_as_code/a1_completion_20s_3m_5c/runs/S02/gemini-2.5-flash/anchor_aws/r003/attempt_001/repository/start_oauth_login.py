import secrets
from urllib.parse import urlencode


def start_oauth_login(payload, config=None):
    config = config or {}
    state = secrets.token_urlsafe(32)
    domain = f"https://{config['domain_prefix']}.auth.{config['region']}.amazoncognito.com"
    query = {"response_type": "code", "client_id": config["client_id"],
             "redirect_uri": payload["redirect_uri"], "scope": "openid email profile", "state": state}
    if config.get("identity_provider"):
        query["identity_provider"] = config["identity_provider"]
    return {"authorization_url": domain + "/oauth2/authorize?" + urlencode(query), "session_id": state}
