import secrets
import msal
from identity_client import get_microsoft_entra_config
from identity_models import TokenResponse


def start_oauth_login(
    scopes: list[str] | None = None,
    redirect_uri: str | None = None,
    state: str | None = None,
    nonce: str | None = None,
) -> tuple[str, str, str]:
    if scopes is None:
        scopes = ["openid", "profile", "email"]
    config = get_microsoft_entra_config(public_client=False)
    if redirect_uri is None:
        redirect_uri = config["redirect_uri"]
    app = msal.ConfidentialClientApplication(
        config["client_id"],
        authority=config["authority"],
        client_credential=config["client_credential"],
    )
    if state is None:
        state = secrets.token_urlsafe(32)
    if nonce is None:
        nonce = secrets.token_urlsafe(32)
    auth_url = app.get_authorization_request_url(
        scopes=scopes, redirect_uri=redirect_uri, state=state, nonce=nonce
    )
    return auth_url, state, nonce
