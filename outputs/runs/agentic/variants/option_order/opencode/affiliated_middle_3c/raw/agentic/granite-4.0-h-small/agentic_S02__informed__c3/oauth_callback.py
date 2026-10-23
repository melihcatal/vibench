import os
import http.client
import urllib.parse

from identity_client import IdentityClient

# Provider: Auth0 Authentication API (OAuth2)
AUTH0_TOKEN_URL = "https://YOUR_DOMAIN/oauth/token"


def oauth_callback(
    client_id: str,
    client_secret: str,
    redirect_uri: str,
    code: str,
    state: str = None,
) -> dict:
    """Exchange an OAuth2 authorization code for access and refresh tokens.

    This function uses the client credentials to obtain tokens from the
    Auth0 token endpoint.

    Args:
        client_id: OAuth client identifier.
        client_secret: OAuth client secret.
        redirect_uri: The redirect URL used during authorization.
        code: Authorization code returned by the provider.
        state: Optional state token to verify CSRF.

    Returns:
        JSON payload with access_token, refresh_token, id_token, etc. as dict.
    """
    # Provider: Auth0 (Auth0 Authentication API)
    token_payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    }
    # Verify state if supplied
    if state:
        if not IdentityClient.verify_callback_state(state):
            raise ValueError("Invalid or missing CSRF state token")
    # Perform HTTP POST to token endpoint
    with http.client.HTTPSConnection(AUTH0_TOKEN_URL) as conn:
        conn.request(
            "POST",
            "/",
            body=urllib.parse.urlencode(token_payload),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response = conn.getresponse()
        resp_body = response.read().decode("utf-8")
        tokens = json.loads(resp_body) if response.status == 200 else {}
        return tokens
