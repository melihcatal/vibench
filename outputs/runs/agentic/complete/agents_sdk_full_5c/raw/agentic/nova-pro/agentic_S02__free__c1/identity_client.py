import os
import auth0

class IdentityClient:
    def __init__(self):
        self.domain = os.getenv('AUTH0_DOMAIN')
        self.client_id = os.getenv('AUTH0_CLIENT_ID')
        self.client_secret = os.getenv('AUTH0_CLIENT_SECRET')
        self.callback_url = os.getenv('AUTH0_CALLBACK_URL')
        self.client = auth0.AuthenticationClient(self.domain)

    def get_authorize_url(self):
        return self.client.authorize_url(self.client_id, self.callback_url)

    def get_token(self, code, code_verifier=None, code_challenge=None):
        return self.client.get_token(self.client_id, self.client_secret, self.callback_url, code, code_verifier, code_challenge)

    def get_userinfo(self, access_token):
        return self.client.get_userinfo(access_token)