import os
import requests
from identity_client import IdentityClient, OkHttpClient
from identity_models import PKCEAuthorizationRequest, PKCETokenExchangeRequest

# Auth0 example for public client (PKCE) flow
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")


def pkce_login(redirect_uri: str) -> str:
    """Generate code_challenge and start PKCE authorization request for a public client.
    Returns the authorization URL with the generated challenge.
    """
    # Generate PKCE code_verifier and derive code_challenge (S256)
    code_verifier = IdentityClient.generate_code_verifier()
    code_challenge = IdentityClient.sha256_base64url(code_verifier)
    auth_req = PKCEAuthorizationRequest(
        client_id=AUTH0_CLIENT_ID,
        response_type="code",
        redirect_uri=redirect_uri,
        scope="openid profile email",
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    auth_url = IdentityClient.build_authorize_url(auth_req)
    return auth_url


def exchange_pkce_code(
    code: str, code_verifier: str, redirect_uri: str
) -> Auth0TokenResponse:
    """Exchange the PKCE authorization code for ID and access tokens.
    Returns an Auth0TokenResponse containing the tokens.
    """
    token_payload = PKCETokenExchangeRequest(
        grant_type="authorization_code",
        client_id=AUTH0_CLIENT_ID,
        code=code,
        redirect_uri=redirect_uri,
        code_verifier=code_verifier,
    )
    token_resp = IdentityClient.exchange_code_for_tokens(token_payload)
    return token_resp
