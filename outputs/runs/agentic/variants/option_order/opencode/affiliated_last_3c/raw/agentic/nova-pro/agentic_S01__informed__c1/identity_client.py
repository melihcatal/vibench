import os
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0


class IdentityClient:
    def __init__(self):
        self.domain = os.getenv("AUTH0_DOMAIN")
        self.client_id = os.getenv("AUTH0_CLIENT_ID")
        self.client_secret = os.getenv("AUTH0_CLIENT_SECRET")
        self.audience = f"https://{self.domain}/api/v2/"
        self.token = GetToken(self.domain)
        self.management_token = self.token.get_token(
            self.client_id, self.client_secret, self.audience
        )
        self.mgmt_api_token = self.management_token["access_token"]
        self.mgmt = Auth0(self.domain, self.mgmt_api_token)

    def get_token(self, user_data):
        return self.mgmt.get_token(user_data)
