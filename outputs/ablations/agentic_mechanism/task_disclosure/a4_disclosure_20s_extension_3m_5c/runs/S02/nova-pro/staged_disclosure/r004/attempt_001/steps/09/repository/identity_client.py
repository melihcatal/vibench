from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

# Configuration
DOMAIN = 'your-domain.auth0.com'
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'

# Client Helper Function
def get_management_token():
    get_token = GetToken(DOMAIN)
    token = get_token.client_credentials(CLIENT_ID, CLIENT_SECRET, 'https://{}/'.format(DOMAIN))
    return token['access_token']

def create_auth0_client():
    management_token = get_management_token()
    return Auth0(DOMAIN, management_token)