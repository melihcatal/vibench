from identity_client import load_identity_client
from identity_models import (
    OAuthRequest,
    create_nonce,
    create_pkce_pair,
    create_state_token,
    pack_session,
)


def start_pkce_login(redirect_uri: str, scope: str = "openid profile email"):
    client = load_identity_client()
    pkce = create_pkce_pair()
    state = create_state_token()
    nonce = create_nonce()
    authorization_url = client.build_authorize_url(
        redirect_uri=redirect_uri,
        state=state,
        nonce=nonce,
        scope=scope,
        code_challenge=pkce["code_challenge"],
    )
    session_blob = pack_session(
        {"state": state, "nonce": nonce, "code_verifier": pkce["code_verifier"]}
    )
    return OAuthRequest(
        authorization_url=authorization_url,
        state=state,
        nonce=nonce,
        code_verifier=pkce["code_verifier"],
        code_challenge=pkce["code_challenge"],
    ), session_blob
