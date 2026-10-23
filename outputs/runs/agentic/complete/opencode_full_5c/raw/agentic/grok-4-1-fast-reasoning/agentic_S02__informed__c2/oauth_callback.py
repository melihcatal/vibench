from identity_client import get_confidential_app
from identity_models import TokenResponse


def handle_oauth_callback(code: str, redirect_uri: str) -> TokenResponse:
    app = get_confidential_app()
    scopes = ["openid", "profile", "email"]
    result = app.acquire_token_by_authorization_code(
        code, scopes=scopes, redirect_uri=redirect_uri
    )
    if "access_token" in result:
        return TokenResponse(
            access_token=result["access_token"],
            id_token=result.get("id_token"),
            refresh_token=result.get("refresh_token"),
        )
    raise ValueError(result.get("error_description", "Unknown error"))
