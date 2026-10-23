import os


class Auth0ClientConfig:
    def __init__(self):
        self.domain = os.getenv("AUTH0_DOMAIN")
        self.client_id = os.getenv("AUTH0_CLIENT_ID")
        self.client_secret = os.getenv("AUTH0_CLIENT_SECRET")
        self.redirect_uri = os.getenv("AUTH0_REDIRECT_URI")
        self.audience = os.getenv("AUTH0_AUDIENCE", f"https://{self.domain}/api/v2/")

    def validate(self):
        if not all([self.domain, self.client_id, self.redirect_uri]):
            raise ValueError("Missing Auth0 configuration environment variables")


def get_auth0_config():
    config = Auth0ClientConfig()
    config.validate()
    return config
