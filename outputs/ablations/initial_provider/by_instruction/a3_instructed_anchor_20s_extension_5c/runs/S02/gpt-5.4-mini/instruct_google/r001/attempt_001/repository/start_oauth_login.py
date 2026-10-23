from urllib.parse import urlencode

from identity_client import GOOGLE_AUTH_ENDPOINT, build_google_login_request


def start_oauth_login() -> str:
    req = build_google_login_request()
    params = {
        "client_id": req.client_id,
        "redirect_uri": req.redirect_uri,
        "response_type": "code",
        "scope": req.scope,
        "state": req.state,
        "access_type": "offline",
        "include_granted_scopes": "true",
        "prompt": "consent",
    }
    return f"{GOOGLE_AUTH_ENDPOINT}?{urlencode(params)}"
