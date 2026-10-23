import os
from auth0.v3.management import Auth0

def get_auth0_management_client():
    domain = os.getenv("AUTH0_DOMAIN")
    client_id = os.getenv("AUTH0_CLIENT_ID")
    client_secret = os.getenv("AUTH0_CLIENT_SECRET")
    
    return Auth0(domain, client_id, client_secret)