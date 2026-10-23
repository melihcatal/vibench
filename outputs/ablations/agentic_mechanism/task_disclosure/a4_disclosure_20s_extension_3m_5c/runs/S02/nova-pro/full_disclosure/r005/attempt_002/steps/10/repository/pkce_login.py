import os
from auth0.v3.authentication import GetToken
from auth0.v3.exceptions import Auth0Error

class PKCELogin:
    def __init__(self):
        self.domain = os.getenv('AUTH0_DOMAIN')
        self.client_id = os.getenv('AUTH0_CLIENT_ID')
        self.client_secret = os.getenv('AUTH0_CLIENT_SECRET')
        self.audience = os.getenv('AUTH0_AUDIENCE')
        self.redirect_uri = os.getenv('AUTH0_REDIRECT_URI')

    def get_authorization_url(self):
        auth0 = GetToken(self.domain)
        try:
            response = auth0.authorization_url(
                audience=self.audience,
                scope='openid profile email',
                response_type='code',
                redirect_uri=self.redirect_uri,
                client_id=self.client_id,
                code_challenge_method='S256'
            )
            return response['authorization_uri']
        except Auth0Error as e:
            print(f'Error getting authorization URL: {e}')
            return None

    def exchange_code_for_tokens(self, code):
        auth0 = GetToken(self.domain)
        try:
            response = auth0.authorization_code(
                client_id=self.client_id,
                client_secret=self.client_secret,
                code=code,
                redirect_uri=self.redirect_uri
            )
            return response
        except Auth0Error as e:
            print(f'Error exchanging code for tokens: {e}')
            return None