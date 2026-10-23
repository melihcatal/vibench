import os
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

class IdentityClient:
    def __init__(self):
        self.domain = os.getenv('AUTH0_DOMAIN')
        self.client_id = os.getenv('AUTH0_CLIENT_ID')
        self.client_secret = os.getenv('AUTH0_CLIENT_SECRET')
        self.mgmt_api_token = self.get_mgmt_api_token()
        self.auth0 = Auth0(self.domain, self.mgmt_api_token)

    def get_mgmt_api_token(self):
        get_token = GetToken(self.domain)
        token = get_token.client_credentials(self.client_id, self.client_secret, 'https://{}/'.format(self.domain))
        return token['access_token']

    def get_user_profile(self, user_id):
        return self.auth0.users.get(user_id)

    def create_user(self, email, password):
        return self.auth0.users.create({'email': email, 'password': password, 'connection': 'Username-Password-Authentication'})

    def delete_user(self, user_id):
        return self.auth0.users.delete(user_id)