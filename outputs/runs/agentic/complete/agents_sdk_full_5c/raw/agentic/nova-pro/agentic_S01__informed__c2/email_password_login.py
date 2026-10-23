import os
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

domain = os.getenv('AUTH0_DOMAIN')
client_id = os.getenv('AUTH0_CLIENT_ID')
client_secret = os.getenv('AUTH0_CLIENT_SECRET')

def email_password_login(email, password):
    mgmt_api_token = GetToken(domain).client_credentials(client_id, client_secret, 'https://{}/'.format(domain) + 'api/v2/')
    management_api_token = mgmt_api_token['access_token']
    mgmt = Auth0(domain, management_api_token)
    tokens = mgmt.token.get(grant_type='password', username=email, password=password, audience='https://{}/'.format(domain) + 'api/v2/', client_id=client_id, client_secret=client_secret)
    return tokens