import os
import secrets
from urllib.parse import urlencode

from identity_client import authorization_endpoint, load_identity_config


def build_login_url(redirect_uri: str | None = None) -> tuple[str, str]:
    config = load_identity_config("AUTH0")
    state = secrets.token_urlsafe(24)
    params = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": redirect_uri
        or config.redirect_uri
        or os.environ.get("AUTH0_REDIRECT_URI", ""),
        "scope": config.scope,
        "state": state,
        "audience": os.environ.get("AUTH0_AUDIENCE", ""),
    }
    return (
        f"{authorization_endpoint(config)}?{urlencode({k: v for k, v in params.items() if v})}",
        state,
    )
