import os
from auth0.v3.authentication import GetToken

def email_password_login(email, password):
    domain = os.getenv('AUTH0_DOMAIN')
    client_id = os.getenv('AUTH0_CLIENT_ID')
    client_secret = os.getenv('AUTH0_CLIENT_SECRET')

    auth0 = GetToken(domain)
    tokens = auth0.password(client_id, client_secret, email, password, 'https://{}/'.format(domain) + 'api/v2/', 'Username-Password-Authentication')
    return tokens