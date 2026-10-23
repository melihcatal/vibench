import os
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

# Configuration
domain = os.getenv('AUTH0_DOMAIN')
client_id = os.getenv('AUTH0_CLIENT_ID')
client_secret = os.getenv('AUTH0_CLIENT_SECRET')

# Auth0 Management API
mgmt_api_token = GetToken(domain).client_credentials(client_id, client_secret, 'https://{}/'.format(domain))
mgmt_api_token = mgmt_api_token.get('access_token')
mgmt = Auth0(domain, mgmt_api_token)

# Identity Client
class IdentityClient:
    def __init__(self):
        self.mgmt = mgmt

    def get_user(self, user_id):
        return self.mgmt.users.get(user_id)