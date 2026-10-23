from identity_client import load_identity_client
from identity_models import OAuthTokenResponse, unpack_session


def handle_oauth_callback(code: str, redirect_uri: str, session_blob: str):
    session = unpack_session(session_blob)
    client = load_identity_client()
    tokens = client.exchange_code(
        code=code, redirect_uri=redirect_uri, code_verifier=session.get("code_verifier")
    )
    return OAuthTokenResponse(
        access_token=tokens["access_token"],
        id_token=tokens.get("id_token"),
        refresh_token=tokens.get("refresh_token"),
        token_type=tokens.get("token_type"),
        expires_in=tokens.get("expires_in"),
        raw=tokens,
    )
