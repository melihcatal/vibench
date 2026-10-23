import secrets

from identity_client import build_authorize_url, exchange_code_for_token
from identity_models import pkce_code_challenge


def start_pkce_login() -> dict:
    code_verifier = secrets.token_urlsafe(64)
    return {
        "authorization_url": build_authorize_url(
            code_challenge=pkce_code_challenge(code_verifier)
        ),
        "code_verifier": code_verifier,
    }


def finish_pkce_login(code: str, code_verifier: str) -> dict:
    return exchange_code_for_token(code, code_verifier=code_verifier)
