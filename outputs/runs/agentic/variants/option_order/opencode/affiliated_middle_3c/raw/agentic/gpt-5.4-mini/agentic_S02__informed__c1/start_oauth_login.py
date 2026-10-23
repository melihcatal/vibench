from identity_client import authorize_url, oidc_session, random_nonce, random_state
from identity_models import LoginRequest


def build_login(redirect_uri: str, scopes=None):
    scopes = scopes or ["openid", "profile", "email"]
    req = LoginRequest(
        redirect_uri=redirect_uri,
        state=random_state(),
        scopes=scopes,
        nonce=random_nonce(),
    )
    session = oidc_session(redirect_uri=req.redirect_uri, scope=req.scopes)
    url, state = session.create_authorization_url(
        authorize_url(), nonce=req.nonce, state=req.state
    )
    return {"authorization_url": url, "state": state, "provider": "auth0"}
