import requests
from identity_client import IdentityClient


def start_oauth_login(client_id, redirect_uri, scope="openid email profile"):
    """Initiate an authorization-code OAuth login flow.

    Uses Auth0 as the concrete external identity provider.
    Returns the authorization URL the user should be redirected to.
    """
    AUTH0_DOMAIN = "your-tenant.auth0.com"
    AUTH0_URL = f"https://{AUTH0_DOMAIN}/authorize"
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "response_mode": "query",
        "prompt": "none",
    }
    auth_url = f"{AUTH0_URL}?{requests.compat.urlencode(params)}"
    return auth_url


if __name__ == "__main__":
    client = IdentityClient()
    url = start_oauth_login(client.client_id, client.redirect_uri)
    print("Redirect user to:", url)
