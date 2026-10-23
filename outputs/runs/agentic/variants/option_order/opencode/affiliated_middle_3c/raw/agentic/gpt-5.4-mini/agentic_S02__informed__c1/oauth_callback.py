from identity_client import oidc_session, token_url
from identity_models import TokenResponse


def exchange_code(
    code: str, redirect_uri: str, code_verifier: str = None
) -> TokenResponse:
    session = oidc_session(
        redirect_uri=redirect_uri, scope=["openid", "profile", "email"]
    )
    token = session.fetch_token(token_url(), code=code, code_verifier=code_verifier)
    return TokenResponse(
        access_token=token["access_token"],
        id_token=token.get("id_token"),
        refresh_token=token.get("refresh_token"),
        expires_in=token.get("expires_in"),
        token_type=token.get("token_type"),
        raw=token,
    )
