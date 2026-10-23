"""
Local helper utilities for configuring and initializing identity provider clients.
"""
import os
import msal
from auth0.management import Auth0

def get_auth0_client() -> Auth0:
    """
    Initializes and returns the Auth0 Management API client.
    Reads configuration from environment variables.
    """
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET")

    if not all([domain, client_id, client_secret]):
        raise ValueError("Auth0 environment variables not set.")

    return Auth0(
        domain=domain,
        client_id=client_id,
        client_secret=client_secret
    )

def get_msal_public_client() -> msal.PublicClientApplication:
    """
    Initializes and returns an MSAL PublicClientApplication for PKCE flows.
    Reads configuration from environment variables.
    """
    client_id = os.environ.get("AZURE_CLIENT_ID")
    tenant_id = os.environ.get("AZURE_TENANT_ID")
    authority = f"https://login.microsoftonline.com/{tenant_id}"

    if not all([client_id, tenant_id]):
        raise ValueError("Azure MSAL environment variables not set.")

    return msal.PublicClientApplication(
        client_id=client_id,
        authority=authority
    )
