from identity_client import auth0_client
from identity_models import OAuthResponse


def pkce_login(redirect_uri: str, state: str, code_verifier: str):
    request = identity_models.OAuthRequest(redirect_uri, state)
    authorization_url = auth0_client.authorize_url(
        redirect_uri=request.redirect_uri,
        state=request.state,
        code_challenge=code_verifier,
        code_challenge_method="S256",
    )
    print(f"Authorization URL: {authorization_url}")
    return authorization_url
