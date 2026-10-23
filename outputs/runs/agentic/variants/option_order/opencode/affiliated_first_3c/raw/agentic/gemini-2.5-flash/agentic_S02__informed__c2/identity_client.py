import os


class IdentityClientConfig:
    def __init__(self):
        self.AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
        self.AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
        self.AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
        self.AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")

    def validate(self):
        if not all([self.AUTH0_DOMAIN, self.AUTH0_CLIENT_ID, self.AUTH0_CALLBACK_URL]):
            raise ValueError(
                "Missing essential Auth0 configuration environment variables."
            )
        if self.AUTH0_CLIENT_SECRET is None:
            print(
                "Warning: AUTH0_CLIENT_SECRET is not set. This may be acceptable for public clients."
            )


def get_auth0_config():
    config = IdentityClientConfig()
    config.validate()
    return config
