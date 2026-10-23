import os

class IdentityClient:
    def __init__(self, domain_prefix, region, client_id, client_secret=None):
        self.domain_prefix = domain_prefix
        self.region = region
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = f"https://{self.domain_prefix}.auth.{self.region}.amazoncognito.com"

    def get_auth_config(self):
        return {
            "domain_prefix": self.domain_prefix,
            "region": self.region,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

    # Add more helper methods for Cognito interactions if needed
