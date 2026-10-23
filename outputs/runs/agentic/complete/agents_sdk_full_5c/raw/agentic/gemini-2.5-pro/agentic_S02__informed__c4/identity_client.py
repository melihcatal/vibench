import os
from auth0.management import Auth0

def get_auth0_client():
    """
    Initializes and returns the Auth0 client from environment variables.
    """
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET")

    if not all([domain, client_id, client_secret]):
        raise ValueError("AUTH0_DOMAIN, AUTH0_CLIENT_ID, and AUTH0_CLIENT_SECRET must be set.")

    # Note: For Authentication API, we often use different classes, 
    # but the core config is the same. This client is for the Management API.
    # The Authentication API client is instantiated directly in the files that need it.
    return Auth0(domain, client_id, client_secret=client_secret)

def get_auth0_config():
    """
    Returns a dictionary of the core Auth0 configuration.
    """
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
    
    if not all([domain, client_id]):
        raise ValueError("AUTH0_DOMAIN and AUTH0_CLIENT_ID must be set.")
        
    return {
        "domain": domain,
        "client_id": client_id,
        "client_secret": client_secret, # May be None for public clients
    }
