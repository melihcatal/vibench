import os


class IdentityClientConfig:
    def __init__(self):
        self.auth0_domain = os.environ.get("AUTH0_DOMAIN")
        self.auth0_client_id = os.environ.get("AUTH0_CLIENT_ID")
        self.auth0_client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
        self.auth0_callback_url = os.environ.get("AUTH0_CALLBACK_URL")

    def is_valid(self):
        return all(
            [
                self.auth0_domain,
                self.auth0_client_id,
                self.auth0_client_secret,
                self.auth0_callback_url,
            ]
        )


class IdentityClient:
    def __init__(self, config: IdentityClientConfig):
        self.config = config
        if not self.config.is_valid():
            raise ValueError("Identity client configuration is incomplete.")

    def get_auth0_base_url(self):
        return f"https://{self.config.auth0_domain}"

    def get_auth0_api_audience(self):
        return f"https://{self.config.auth0_domain}/api/v2/"


# This file can be extended with more helper utilities as needed,
# e.g., for generating state parameters, handling nonces, etc.
