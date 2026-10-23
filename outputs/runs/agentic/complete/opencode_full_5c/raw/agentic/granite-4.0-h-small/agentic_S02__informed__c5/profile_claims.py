import requests
from identity_client import IdentityClient

# Reference concrete provider: Auth0 Authentication API
# Provider identifiers: AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET


def start_oauth_login(redirect_uri: str, scopes: list[str] = None) -> str:
    """Redirect user to Auth0 authorization endpoint to begin OAuth login.

    Args:
        redirect_uri: The URL the user will be sent back to after login.
        scopes: OAuth scopes to request (default includes openid profile email).

    Returns:
        The full authorization URL.
    """
    if scopes is None:
        scopes = ["openid", "profile", "email"]
    # URL template for Auth0 authorization
    AUTH0_DOMAIN = IdentityClient.get_config("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = IdentityClient.get_config("AUTH0_CLIENT_ID")
    url = (
        f"https://{AUTH0_DOMAIN}/authorize?"
        f"response_type=code&client_id={AUTH0_CLIENT_ID}&redirect_uri={redirect_uri}&scope={'%20'.join(scopes)}&response_mode=query"
    )
    return url


def oauth_callback(request: dict) -> dict:
    """Exchange an authorization code for tokens using Auth0 token endpoint.
    The request dict is expected to contain a 'code' field from the query string.
    """
    AUTH0_DOMAIN = IdentityClient.get_config("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = IdentityClient.get_config("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = IdentityClient.get_config("AUTH0_CLIENT_SECRET")
    code = request.get("code")
    if not code:
        raise ValueError("Authorization code missing in request")
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": IdentityClient.get_config("AUTH0_REDIRECT_URI"),
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
    }
    response = requests.post(token_url, data=payload)
    response.raise_for_status()
    return response.json()


def profile_claims(id_token: str) -> dict:
    """Parse and normalize federated user profile claims from an ID token.
    The ID token is a JWT issued by Auth0.
    """
    # Simple JWT decoding (no verification) – for production use a library like python-jose
    import jwt

    # No verification keys – in real code load JWKs from Auth0 well‑known endpoint
    header = jwt.get_unverified_header(id_token)
    payload = jwt.get_unverified_claims(id_token)
    # Normalize claims to a common structure
    return {
        "subject": payload.get("sub"),
        "email": payload.get("email"),
        "email_verified": payload.get("email_verified"),
        "name": payload.get("name"),
        "given_name": payload.get("given_name"),
        "family_name": payload.get("family_name"),
        # Add any additional normalized fields here...
    }
