import os
from typing import Dict, Any

class IdentityClientConfig:
    """
    Configuration helper for Auth0 integration.
    Loads necessary environment variables.
    """
    def __init__(self):
        self.AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
        self.AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
        self.AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
        self.AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL")

        if not all([self.AUTH0_DOMAIN, self.AUTH0_CLIENT_ID, self.AUTH0_CALLBACK_URL]):
            raise ValueError("Auth0_DOMAIN, AUTH0_CLIENT_ID, and AUTH0_CALLBACK_URL must be set.")

    def get_auth0_config(self) -> Dict[str, Any]:
        return {
            "domain": self.AUTH0_DOMAIN,
            "client_id": self.AUTH0_CLIENT_ID,
            "client_secret": self.AUTH0_CLIENT_SECRET,
            "callback_url": self.AUTH0_CALLBACK_URL,
        }

def load_auth0_config() -> IdentityClientConfig:
    """
    Helper function to load and return the Auth0 configuration.
    """
    return IdentityClientConfig()

if __name__ == "__main__":
    # Example usage
    os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.us.auth0.com"
    os.environ["AUTH0_CLIENT_ID"] = "YOUR_AUTH0_CLIENT_ID"
    os.environ["AUTH0_CLIENT_SECRET"] = "YOUR_AUTH0_CLIENT_SECRET"
    os.environ["AUTH0_CALLBACK_URL"] = "http://localhost:8000/callback"

    try:
        config = load_auth0_config()
        print("Auth0 Configuration Loaded:")
        print(config.get_auth0_config())
    except ValueError as e:
        print(f"Error loading configuration: {e}")
