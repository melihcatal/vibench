import secrets
import webbrowser
from urllib.parse import urlencode
from .identity_client import get_google_confidential_config
from .identity_models import OAuthConfig


def generate_standard_auth_url(config: OAuthConfig) -> str:
    state = secrets.token_urlsafe(32)
    nonce = secrets.token_urlsafe(32)
    params = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "scope": " ".join(config.scopes),
        "response_type": "code",
        "state": state,
        "nonce": nonce,
    }
    url = config.auth_url + "?" + urlencode(params)
    return url


def start_oauth_login():
    config = get_google_confidential_config()
    url = generate_standard_auth_url(config)
    print(f"Opening Google OAuth URL: {url}")
    webbrowser.open(url)
