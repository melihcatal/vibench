import os

class Auth0ClientConfig:
    def __init__(self):
        self.domain = os.environ.get("AUTH0_DOMAIN")
        self.client_id = os.environ.get("AUTH0_CLIENT_ID")
        self.client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
        self.callback_url = os.environ.get("AUTH0_CALLBACK_URL")
        self.audience = f"https://{self.domain}/api/v2/" if self.domain else None

    def validate(self):
        if not all([self.domain, self.client_id, self.callback_url]):
            raise ValueError("Missing essential Auth0 configuration: DOMAIN, CLIENT_ID, CALLBACK_URL")

    def __repr__(self):
        return (
            f"Auth0ClientConfig(domain='{self.domain}', client_id='{self.client_id}', "
            f"callback_url='{self.callback_url}', audience='{self.audience}')"
        )


def get_auth0_config() -> Auth0ClientConfig:
    config = Auth0ClientConfig()
    config.validate()
    return config

if __name__ == '__main__':
    # Example usage:
    # export AUTH0_DOMAIN="YOUR_AUTH0_DOMAIN"
    # export AUTH0_CLIENT_ID="YOUR_AUTH0_CLIENT_ID"
    # export AUTH0_CLIENT_SECRET="YOUR_AUTH0_CLIENT_SECRET" # Optional for some flows
    # export AUTH0_CALLBACK_URL="http://localhost:8000/callback"
    # try:
    #     config = get_auth0_config()
    #     print(config)
    # except ValueError as e:
    #     print(f"Configuration Error: {e}")
    pass
