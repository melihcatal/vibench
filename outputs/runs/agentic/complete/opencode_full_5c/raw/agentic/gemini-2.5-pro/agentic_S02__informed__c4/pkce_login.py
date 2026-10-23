import os
import hashlib
import base64
from auth0.authentication import GetToken
from identity_client import get_auth0_config
from identity_models import TokenResponse


def generate_pkce_challenge():
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode("utf-8")
    code_verifier = code_verifier.rstrip("=")

    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
    code_challenge = code_challenge.rstrip("=")

    return code_verifier, code_challenge


def start_pkce_login(redirect_uri: str, state: str, code_challenge: str) -> str:
    config = get_auth0_config()
    auth0_client = GetToken(config["domain"])

    authorize_url = auth0_client.authorization_url(
        client_id=config["client_id"],
        redirect_uri=redirect_uri,
        response_type="code",
        scope="openid profile email",
        state=state,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    return authorize_url


def exchange_pkce_code(
    code: str, redirect_uri: str, code_verifier: str
) -> TokenResponse:
    config = get_auth0_config()
    auth0_client = GetToken(config["domain"])

    token_data = auth0_client.authorization_code(
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        code=code,
        redirect_uri=redirect_uri,
        code_verifier=code_verifier,
    )
    return TokenResponse(**token_data)
