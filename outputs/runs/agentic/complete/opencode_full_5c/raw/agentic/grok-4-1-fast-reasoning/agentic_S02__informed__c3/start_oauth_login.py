import webbrowser
import secrets
from urllib.parse import urlencode
from identity_client import get_auth_config
from identity_models import AuthConfig


def generate_state() -> str:
    return secrets.token_urlsafe(32)


def start_oauth_login() -> str:
    config = get_auth_config()
    state = generate_state()
    params = {
        "client_id": config.client_id,
        "response_type": "code",
        "scope": "openid profile email",
        "redirect_uri": config.redirect_uri,
        "state": state,
    }
    auth_url = f"https://{config.domain}/oauth2/authorize?{urlencode(params)}"
    print(f"Generated state: {state}")
    print(f"Authorization URL: {auth_url}")
    webbrowser.open(auth_url)
    return state
