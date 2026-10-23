import os
from auth0.v3.authentication import GetToken

def refresh_session(refresh_token):
    domain = os.getenv('AUTH0_DOMAIN')
    client_id = os.getenv('AUTH0_CLIENT_ID')
    client_secret = os.getenv('AUTH0_CLIENT_SECRET')

    auth0 = GetToken(domain)
    tokens = auth0.refresh_token(client_id, client_secret, refresh_token, 'https://{}/'.format(domain) + 'api/v2/')
    return tokens