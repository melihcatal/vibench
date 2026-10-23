import os

COGNITO_DOMAIN = os.getenv('COGNITO_DOMAIN')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')
COGNITO_CLIENT_SECRET = os.getenv('COGNITO_CLIENT_SECRET')

class IdentityClient:
    def __init__(self):
        self.cognito_domain = COGNITO_DOMAIN
        self.client_id = COGNITO_CLIENT_ID
        self.client_secret = COGNITO_CLIENT_SECRET