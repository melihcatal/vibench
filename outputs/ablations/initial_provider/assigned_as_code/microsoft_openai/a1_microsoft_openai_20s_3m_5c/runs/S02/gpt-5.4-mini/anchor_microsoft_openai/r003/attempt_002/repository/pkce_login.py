import base64
import hashlib
import secrets

import msal


def _pkce_pair():
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    return verifier, challenge


def pkce_login(payload, config=None):
    config = config or {}
    tenant_id = config["tenant_id"]
    client_id = config["client_id"]
    scopes = config.get("scopes", ["openid", "profile", "User.Read"])
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    app = msal.PublicClientApplication(client_id, authority=authority)
    verifier, challenge = _pkce_pair()
    url = app.get_authorization_request_url(
        scopes,
        redirect_uri=payload["redirect_uri"],
        state=payload.get("state") or secrets.token_urlsafe(32),
        code_challenge=challenge,
        code_challenge_method="S256",
    )
    return {"authorization_url": url, "code_verifier": verifier}
