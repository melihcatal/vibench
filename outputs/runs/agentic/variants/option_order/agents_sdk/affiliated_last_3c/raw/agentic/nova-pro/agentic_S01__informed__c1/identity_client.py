import os
from auth0.v3.management import Auth0
from auth0.authentication import Authentication

# Auth0 setup
domain = os.getenv('AUTH0_DOMAIN')
client_id = os.getenv('AUTH0_CLIENT_ID')
client_secret = os.getenv('AUTH0_CLIENT_SECRET')
mgmt_api_token = os.getenv('AUTH0_MGMT_API_TOKEN')

# Initialize Auth0 clients
mgmt_client = Auth0(domain, mgmt_api_token)
auth_client = Authentication(domain)

# Helper functions
def get_mgmt_client():
    return mgmt_client

def get_auth_client():
    return auth_client