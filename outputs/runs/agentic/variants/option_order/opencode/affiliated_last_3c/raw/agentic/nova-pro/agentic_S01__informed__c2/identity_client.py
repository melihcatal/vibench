import os

# Configuration
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")


class IdentityClient:
    def __init__(self):
        self.domain = AUTH0_DOMAIN
        self.client_id = AUTH0_CLIENT_ID
        self.client_secret = AUTH0_CLIENT_SECRET

    def get_mgmt_api_token(self):
        from auth0.v3.authentication import GetToken

        token = GetToken(self.domain).client_credentials(
            self.client_id, self.client_secret, "https://{}/".format(self.domain)
        )
        return token["access_token"]

    def get_auth0_client(self):
        from auth0.v3.management import Auth0

        token = self.get_mgmt_api_token()
        return Auth0(self.domain, token)
