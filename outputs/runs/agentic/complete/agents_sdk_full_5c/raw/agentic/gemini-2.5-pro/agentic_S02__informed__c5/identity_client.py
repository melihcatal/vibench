import os
from auth0.authentication import AuthenticationAPI
from msal import PublicClientApplication

def get_auth0_client():
    """Initializes and returns an Auth0 AuthenticationAPI client."""
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
    
    if not all([domain, client_id, client_secret]):
        raise ValueError("Auth0 environment variables are not set.")

    return AuthenticationAPI(
        domain=domain,
        client_id=client_id,
        client_secret=client_secret
    )

def get_auth0_config():
    """Returns Auth0 configuration values."""
    return {
        "domain": os.environ.get("AUTH0_DOMAIN"),
        "client_id": os.environ.get("AUTH0_CLIENT_ID"),
        "callback_url": os.environ.get("AUTH0_CALLBACK_URL", "http://localhost:3000/callback")
    }

def get_msal_client():
    """Initializes and returns an MSAL PublicClientApplication."""
    client_id = os.environ.get("AZURE_CLIENT_ID")
    authority = os.environ.get("AZURE_AUTHORITY_URL") # e.g., https://login.microsoftonline.com/your_tenant_id

    if not all([client_id, authority]):
        raise ValueError("Azure AD environment variables are not set.")

    return PublicClientApplication(
        client_id=client_id,
        authority=authority
    )

def get_msal_config():
    """Returns MSAL configuration values."""
    return {
        "redirect_uri": os.environ.get("AZURE_REDIRECT_URI", "http://localhost:3000/redirect"),
        "scope": os.environ.get("AZURE_SCOPES", "User.Read").split(" ")
    }
