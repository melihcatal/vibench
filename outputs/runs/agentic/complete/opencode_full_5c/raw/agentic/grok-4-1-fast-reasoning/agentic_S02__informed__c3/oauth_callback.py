from urllib.parse import urlparse, parse_qs
from identity_client import get_auth_config, exchange_authorization_code
from identity_models import Tokens


def handle_oauth_callback(callback_url: str, expected_state: str = None) -> Tokens:
    parsed = urlparse(callback_url)
    params = parse_qs(parsed.query)
    code = params.get("code", [None])[0]
    state = params.get("state", [None])[0]
    if expected_state and state != expected_state:
        raise ValueError("State mismatch")
    if not code:
        raise ValueError("No authorization code in callback URL")
    config = get_auth_config()
    return exchange_authorization_code(config, code)
