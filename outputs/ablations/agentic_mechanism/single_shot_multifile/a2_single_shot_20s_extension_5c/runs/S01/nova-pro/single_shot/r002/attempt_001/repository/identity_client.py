import os

def get_auth0_management_token():
    domain = os.getenv('AUTH0_DOMAIN')
    client_id = os.getenv('AUTH0_CLIENT_ID')
    client_secret = os.getenv('AUTH0_CLIENT_SECRET')
    from auth0.v3.authentication import GetToken
    token = GetToken(domain).client_credentials(client_id, client_secret, 'https://{}/'.format(domain) + 'api/v2/')
    return token.get('access_token')

def get_auth0_api():
    domain = os.getenv('AUTH0_DOMAIN')
    token = get_auth0_management_token()
    from auth0.v3.management import Auth0
    return Auth0(domain, token)