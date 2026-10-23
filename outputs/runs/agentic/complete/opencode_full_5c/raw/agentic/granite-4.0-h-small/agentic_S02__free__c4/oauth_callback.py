import requests
from identity_client import IdentityClient
from identity_models import OAuthCallbackResponse


def exchange_code_for_tokens(code, redirect_uri, client_id, client_secret):
    """Exchange an authorization code for access and ID tokens using Auth0's token endpoint.

    Uses Auth0 as the concrete external identity provider.
    Returns OAuthCallbackResponse containing tokens and decoded ID token claims.
    """
    AUTH0_DOMAIN = "your-tenant.auth0.com"
    TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    }
    resp = requests.post(TOKEN_URL, data=payload)
    resp.raise_for_status()
    data = resp.json()
    # Decode ID token (JWT) manually or with a helper
    id_token = data.get("id_token")
    decoded_claims = None  # placeholder for JWT decoding logic
    return OAuthCallbackResponse(
        access_token=data["access_token"],
        id_token=id_token,
        token_type=data["token_type"],
        expires_in=data.get("expires_in"),
        claims=decoded_claims,
    )


if __name__ == "__main__":
    # Example usage with values from IdentityClient configuration
    client = IdentityClient()
    # In real app these would come from request parameters
    code = "AUTHORIZATION_CODE_FROM_REDIRECT"
    response = exchange_code_for_tokens(
        code, client.redirect_uri, client.client_id, client.client_secret
    )
    print("Tokens received:", response)
