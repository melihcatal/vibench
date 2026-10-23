import os
from authlib.integrations.httpx_client import OAuth2Client
from dotenv import load_dotenv

load_dotenv()

def get_okta_client() -> OAuth2Client:
    """
    Initializes and returns an Authlib OAuth2Client for Okta.
    """
    okta_domain = os.getenv("OKTA_DOMAIN")
    if not okta_domain:
        raise ValueError("OKTA_DOMAIN environment variable not set.")

    metadata_url = f"https://{okta_domain}/.well-known/openid-configuration"

    client = OAuth2Client(
        client_id=os.getenv("OKTA_CLIENT_ID"),
        client_secret=os.getenv("OKTA_CLIENT_SECRET"),
        scope=os.getenv("OKTA_SCOPES", "openid profile email offline_access"),
        redirect_uri=os.getenv("OKTA_REDIRECT_URI"),
        metadata_url=metadata_url,
    )
    return client
