import base64
import hashlib
import os

from auth0.authentication import AuthorizeClient, GetToken
from identity_client import identity_client
from identity_models import OAuthTokenResponse


def generate_pkce_codes():
    """Generates a code verifier and challenge for PKCE."""
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode("utf-8")
    code_verifier = code_verifier.rstrip("=")
    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
    code_challenge = code_challenge.rstrip("=")
    return code_verifier, code_challenge


def get_pkce_auth_url(session_state: str):
    """Generates an Auth0 authorization URL for a PKCE flow."""
    config = identity_client.get_auth0_config()
    _, code_challenge = generate_pkce_codes()

    authorize = AuthorizeClient(config["domain"])

    return authorize.authorize_url(
        client_id=config["client_id"],
        redirect_uri=config["redirect_uri"],
        response_type="code",
        scope="openid profile email offline_access",
        state=session_state,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )


def exchange_pkce_code_for_token(
    authorization_code: str, code_verifier: str
) -> OAuthTokenResponse:
    """Exchanges an authorization code for tokens using PKCE."""
    config = identity_client.get_auth0_config()
    get_token = GetToken(config["domain"])

    token_data = get_token.authorization_code(
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        code=authorization_code,
        redirect_uri=config["redirect_uri"],
        code_verifier=code_verifier,
    )

    return OAuthTokenResponse(
        access_token=token_data.get("access_token"),
        id_token=token_data.get("id_token"),
        token_type=token_data.get("token_type"),
        expires_in=token_data.get("expires_in"),
        scope=token_data.get("scope"),
        refresh_token=token_data.get("refresh_token"),
    )
