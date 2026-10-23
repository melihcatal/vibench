import os
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

def register_user(email, password):
    domain = os.getenv('AUTH0_DOMAIN')
    client_id = os.getenv('AUTH0_CLIENT_ID')
    client_secret = os.getenv('AUTH0_CLIENT_SECRET')

    mgmt_api_token = GetToken(domain).client_credentials(client_id, client_secret, 'https://{}/'.format(domain) + 'api/v2/')
    mgmt_api_token = mgmt_api_token.get('access_token')
    mgmt_api = Auth0(domain, mgmt_api_token)

    user_data = {
        'email': email,
        'password': password,
        'connection': 'Username-Password-Authentication'
    }

    user = mgmt_api.users.create(user_data)
    return user