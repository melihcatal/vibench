import msal
from identity_client import get_config
from identity_models import TokenResponse

config = get_config()

app = msal.PublicClientApplication(
    config["client_id"],
    authority=config["authority"]
)

def handle_oauth_callback(code: str, state: str):
    result = app.acquire_token_by_authorization_code(
        code,
        scopes=config["scopes"],
        redirect_uri=config["redirect_uri"]
    )
    if "access_token" in result:
        return TokenResponse(
            access_token=result["access_token"],
            id_token=result["id_token"],
            refresh_token=result.get("refresh_token"),
            expires_in=result.get("expires_in")
        )
    else:
        raise ValueError(result.get("error_description"))

# Provider-specific: msal SDK, Microsoft Entra OIDC