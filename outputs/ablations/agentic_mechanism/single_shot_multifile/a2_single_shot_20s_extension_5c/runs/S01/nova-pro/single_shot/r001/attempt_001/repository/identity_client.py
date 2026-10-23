import os
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

def get_management_api_token():
    domain = os.getenv('AUTH0_DOMAIN')
    client_id = os.getenv('AUTH0_CLIENT_ID')
    client_secret = os.getenv('AUTH0_CLIENT_SECRET')

    get_token = GetToken(domain)
    token = get_token.client_credentials(client_id, client_secret, 'https://{}/'.format(domain))
    return token['access_token']

def get_auth0_mgmt_client():
    domain = os.getenv('AUTH0_DOMAIN')
    management_api_token = get_management_api_token()
    return Auth0(domain, management_api_token)