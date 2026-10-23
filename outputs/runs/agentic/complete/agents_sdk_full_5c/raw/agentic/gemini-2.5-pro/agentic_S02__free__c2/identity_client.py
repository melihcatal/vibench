import os
from authlib.integrations.httpx_client import OAuth2Client

def get_okta_client():
    """Initializes and returns an Okta OAuth2 client."""
    okta_domain = os.environ.get("OKTA_DOMAIN")
    if not okta_domain:
        raise ValueError("OKTA_DOMAIN environment variable not set.")

    client = OAuth2Client(
        client_id=os.environ.get("OKTA_CLIENT_ID"),
        client_secret=os.environ.get("OKTA_CLIENT_SECRET"),
        scope="openid profile email",
        redirect_uri=os.environ.get("OKTA_REDIRECT_URI", "http://localhost:8080/callback"),
        metadata_url=f"https://{okta_domain}/.well-known/openid-configuration"
    )
    return client

def get_auth0_config():
    """Returns Auth0 configuration details."""
    auth0_domain = os.environ.get("AUTH0_DOMAIN")
    if not auth0_domain:
        raise ValueError("AUTH0_DOMAIN environment variable not set.")
        
    return {
        "domain": auth0_domain,
        "client_id": os.environ.get("AUTH0_CLIENT_ID"),
        "redirect_uri": os.environ.get("AUTH0_REDIRECT_URI", "http://localhost:8080/pkce-callback"),
        "audience": os.environ.get("AUTH0_AUDIENCE"),
        "metadata_url": f"https://{auth0_domain}/.well-known/openid-configuration"
    }
