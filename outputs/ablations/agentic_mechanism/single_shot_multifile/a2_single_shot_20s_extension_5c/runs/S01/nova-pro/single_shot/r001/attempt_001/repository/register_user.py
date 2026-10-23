import os
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

def register_user(email, password):
    domain = os.getenv('AUTH0_DOMAIN')
    client_id = os.getenv('AUTH0_CLIENT_ID')
    client_secret = os.getenv('AUTH0_CLIENT_SECRET')

    get_token = GetToken(domain)
    token = get_token.client_credentials(client_id, client_secret, 'https://{}/'.format(domain))
    management_api_token = token['access_token']

    mgmt_api = Auth0(domain, management_api_token)
    user = mgmt_api.users.create({
        'email': email,
        'password': password,
        'connection': 'Username-Password-Authentication',
        'email_verified': False,
        'app_metadata': {},
        'user_metadata': {}
    })
    return user