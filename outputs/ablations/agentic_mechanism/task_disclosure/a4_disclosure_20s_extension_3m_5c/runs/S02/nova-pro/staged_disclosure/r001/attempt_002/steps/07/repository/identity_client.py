import os
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

# Load environment variables
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')

# Initialize Auth0 client
def get_auth0_client():
    management_api_token = GetToken(AUTH0_DOMAIN)
    token_info = management_api_token.client_credentials(AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, 'https://{}/'.format(AUTH0_DOMAIN))
    management_api_token = token_info['access_token']
    return Auth0(AUTH0_DOMAIN, management_api_token)
