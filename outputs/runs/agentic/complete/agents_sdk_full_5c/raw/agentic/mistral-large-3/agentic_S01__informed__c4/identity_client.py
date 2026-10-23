import os
from typing import Optional, Dict, Any

class IdentityClientConfig:
    def __init__(self):
        self.domain = os.getenv("AUTH0_DOMAIN")
        self.client_id = os.getenv("AUTH0_CLIENT_ID")
        self.client_secret = os.getenv("AUTH0_CLIENT_SECRET")
        self.audience = f"https://{self.domain}/api/v2/"

    def validate(self) -> None:
        if not self.domain or not self.client_id or not self.client_secret:
            raise ValueError("Missing required Auth0 configuration environment variables.")


def load_identity_client_config() -> IdentityClientConfig:
    config = IdentityClientConfig()
    config.validate()
    return config