import webbrowser
import secrets
import hashlib
import base64
from urllib.parse import urlencode, urlparse, parse_qs
from identity_client import get_auth_config, exchange_authorization_code
from identity_models import Tokens


def generate_pkce_pair() -> tuple[str, str]:
    verifier = (
        base64.urlsafe_b64encode(secrets.token_bytes(32)).decode("utf-8").rstrip("=")
    )
    challenge_bytes = hashlib.sha256(verifier.encode("ascii")).digest()
    challenge = base64.urlsafe_b64encode(challenge_bytes).decode("ascii").rstrip("=")
    return verifier, challenge


def start_pkce_login() -> tuple[str, str]:
    config = get_auth_config()
    verifier, challenge = generate_pkce_pair()
    state = secrets.token_urlsafe(32)
    params = {
        "client_id": config.client_id,
        "response_type": "code",
        "scope": "openid profile email",
        "redirect_uri": config.redirect_uri,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    auth_url = f"https://{config.domain}/oauth2/authorize?{urlencode(params)}"
    print(f"PKCE verifier (save for exchange): {verifier}")
    print(f"Generated state: {state}")
    print(f"Authorization URL: {auth_url}")
    webbrowser.open(auth_url)
    return state, verifier


def handle_pkce_callback(
    callback_url: str, verifier: str, expected_state: str = None
) -> Tokens:
    parsed = urlparse(callback_url)
    params = parse_qs(parsed.query)
    code = params.get("code", [None])[0]
    state = params.get("state", [None])[0]
    if expected_state and state != expected_state:
        raise ValueError("State mismatch")
    if not code:
        raise ValueError("No authorization code in callback")
    config = get_auth_config()
    return exchange_authorization_code(config, code, verifier)
