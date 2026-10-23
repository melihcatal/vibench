from identity_client import exchange_code, load_config
from identity_models import TokenResponse


def oauth_callback(code: str, redirect_uri: str) -> TokenResponse:
    config = load_config()
    token_data = exchange_code(
        config.auth0_domain,
        {
            "grant_type": "authorization_code",
            "client_id": config.auth0_client_id,
            "client_secret": config.auth0_client_secret or "",
            "code": code,
            "redirect_uri": redirect_uri,
        },
    )
    return TokenResponse(
        access_token=token_data["access_token"],
        id_token=token_data.get("id_token", ""),
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data.get("expires_in"),
        raw=token_data,
    )
