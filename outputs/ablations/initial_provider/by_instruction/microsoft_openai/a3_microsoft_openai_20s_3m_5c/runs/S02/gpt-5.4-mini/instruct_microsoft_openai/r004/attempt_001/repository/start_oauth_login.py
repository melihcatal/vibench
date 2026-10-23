import secrets
from urllib.parse import urlencode

from identity_client import microsoft_authorize_url, oauth_request


def build_login_url(redirect_uri: str) -> str:
    state = secrets.token_urlsafe(24)
    verifier = secrets.token_urlsafe(48)
    request = oauth_request(redirect_uri, state, verifier)
    params = {
        "client_id": __import__("identity_client").identity_client.microsoft_client_id(),
        "response_type": "code",
        "redirect_uri": request.redirect_uri,
        "response_mode": "query",
        "scope": "openid profile email offline_access",
        "state": request.state,
        "code_challenge": request.code_challenge,
        "code_challenge_method": "S256",
    }
    return f"{microsoft_authorize_url()}?{urlencode(params)}"
