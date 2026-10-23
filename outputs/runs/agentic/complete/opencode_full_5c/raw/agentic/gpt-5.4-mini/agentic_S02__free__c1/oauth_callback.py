from identity_client import create_oauth_session, load_identity_provider_config
from identity_models import AuthorizationCodeRequest, TokenResponse


def oauth_callback(request: AuthorizationCodeRequest) -> TokenResponse:
    config = load_identity_provider_config("OIDC")
    session = create_oauth_session(config, state=request.state)
    token = session.fetch_token(config.token_endpoint, code=request.code)
    return TokenResponse(
        access_token=token["access_token"],
        id_token=token.get("id_token"),
        refresh_token=token.get("refresh_token"),
        token_type=token.get("token_type", "Bearer"),
        expires_in=token.get("expires_in"),
        raw=token,
    )
