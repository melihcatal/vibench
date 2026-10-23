import os
from typing import Dict, Any
from auth0.authentication import Database
from auth0.management import Auth0


def get_identity_client() -> Database:
    domain = os.getenv("AUTH0_DOMAIN")
    client_id = os.getenv("AUTH0_CLIENT_ID")
    client_secret = os.getenv("AUTH0_CLIENT_SECRET")
    
    return Database(domain, client_id, client_secret)


def get_management_client() -> Auth0:
    domain = os.getenv("AUTH0_DOMAIN")
    client_id = os.getenv("AUTH0_MANAGEMENT_CLIENT_ID")
    client_secret = os.getenv("AUTH0_MANAGEMENT_CLIENT_SECRET")
    
    return Auth0(domain, client_id, client_secret)