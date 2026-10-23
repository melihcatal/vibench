from identity_client import (
    authorize_url,
    oidc_session,
    pkce_challenge,
    pkce_verifier,
    random_state,
)


def build_pkce_login(redirect_uri: str, scopes=None):
    scopes = scopes or ["openid", "profile", "email"]
    verifier = pkce_verifier()
    session = oidc_session(redirect_uri=redirect_uri, scope=scopes)
    url, state = session.create_authorization_url(
        authorize_url(),
        state=random_state(),
        code_challenge=pkce_challenge(verifier),
        code_challenge_method="S256",
    )
    return {
        "authorization_url": url,
        "state": state,
        "code_verifier": verifier,
        "provider": "auth0",
    }
