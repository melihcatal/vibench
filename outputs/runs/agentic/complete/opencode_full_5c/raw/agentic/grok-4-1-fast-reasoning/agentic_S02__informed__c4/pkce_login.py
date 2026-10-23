import secrets
import msal
from msal import crypto
from identity_client import get_microsoft_entra_config
from identity_models import TokenResponse


def start_pkce_login(
    scopes: list[str] | None = None,
    redirect_uri: str | None = None,
    state: str | None = None,
    nonce: str | None = None,
) -> tuple[str, str, str, str, str]:
    if scopes is None:
        scopes = ["openid", "profile", "email"]
    config = get_microsoft_entra_config(public_client=True)
    if redirect_uri is None:
        redirect_uri = config["redirect_uri"]
    app = msal.PublicClientApplication(
        config["client_id"], authority=config["authority"]
    )
    if state is None:
        state = secrets.token_urlsafe(32)
    if nonce is None:
        nonce = secrets.token_urlsafe(32)
    code_challenge, code_verifier = crypto.generate_code_challenge(
        crypto.generate_code_verifier()
    )
    auth_url = app.get_authorization_request_url(
        scopes=scopes,
        redirect_uri=redirect_uri,
        state=state,
        nonce=nonce,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    return auth_url, state, nonce, code_verifier, code_challenge


def pkce_callback(
    authorization_code: str,
    state_received: str,
    expected_state: str,
    code_verifier: str,
    scopes: list[str],
    redirect_uri: str | None = None,
) -> TokenResponse:
    if state_received != expected_state:
        raise ValueError("State mismatch")
    config = get_microsoft_entra_config(public_client=True)
    if redirect_uri is None:
        redirect_uri = config["redirect_uri"]
    app = msal.PublicClientApplication(
        config["client_id"], authority=config["authority"]
    )
    result = app.acquire_token_by_authorization_code(
        authorization_code,
        scopes=scopes,
        redirect_uri=redirect_uri,
        code_verifier=code_verifier,
    )
    if "access_token" not in result:
        raise ValueError(
            f"Token acquisition failed: {result.get('error_description', 'Unknown error')}"
        )
    return TokenResponse(
        access_token=result["access_token"],
        id_token=result["id_token"],
        refresh_token=result.get("refresh_token"),
        expires_in=result.get("expires_in"),
    )
