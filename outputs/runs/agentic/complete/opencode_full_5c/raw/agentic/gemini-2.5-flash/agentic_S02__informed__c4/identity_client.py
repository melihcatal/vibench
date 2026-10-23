import os


class Auth0ClientConfig:
    """
    Configuration utility for Auth0 client.
    Loads environment variables for Auth0 integration.
    """

    def __init__(self):
        self.domain = os.getenv("AUTH0_DOMAIN")
        self.client_id = os.getenv("AUTH0_CLIENT_ID")
        self.client_secret = os.getenv("AUTH0_CLIENT_SECRET")
        self.callback_url = os.getenv("AUTH0_CALLBACK_URL")
        self.audience = os.getenv("AUTH0_AUDIENCE")

        if not all([self.domain, self.client_id, self.callback_url]):
            print(
                "Warning: Auth0 environment variables (AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CALLBACK_URL) are not fully set."
            )

    def get_domain(self):
        return self.domain

    def get_client_id(self):
        return self.client_id

    def get_client_secret(self):
        return self.client_secret

    def get_callback_url(self):
        return self.callback_url

    def get_audience(self):
        return self.audience


if __name__ == "__main__":
    # Example usage:
    config = Auth0ClientConfig()
    print(f"Auth0 Domain: {config.get_domain()}")
    print(f"Auth0 Client ID: {config.get_client_id()}")
    print(f"Auth0 Callback URL: {config.get_callback_url()}")
