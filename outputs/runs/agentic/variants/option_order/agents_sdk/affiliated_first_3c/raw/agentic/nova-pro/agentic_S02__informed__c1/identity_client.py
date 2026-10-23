import os

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')

class IdentityClient:
    def __init__(self):
        self.domain = AUTH0_DOMAIN
        self.client_id = AUTH0_CLIENT_ID
        self.client_secret = AUTH0_CLIENT_SECRET