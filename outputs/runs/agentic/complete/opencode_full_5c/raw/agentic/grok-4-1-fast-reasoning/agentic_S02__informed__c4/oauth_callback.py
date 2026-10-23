import msal
from identity_client import get_microsoft_entra_config
from identity_models import TokenResponse


def oauth_callback(
    authorization_code: str,
    state_received: str,
    expected_state: str,
    scopes: list[str] | None = None,
    redirect_uri: str | None = None,
) -> TokenResponse:
    if state_received != expected_state:
        raise ValueError("State mismatch")
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
    result = app.acquire_token_by_authorization_code(
        authorization_code, scopes=scopes, redirect_uri=redirect_uri
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
