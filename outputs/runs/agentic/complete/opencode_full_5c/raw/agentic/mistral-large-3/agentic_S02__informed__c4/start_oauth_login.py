import os
from typing import Dict, Any
from identity_client import FederatedIdentityClient


class OAuthLoginStarter:
    def __init__(self):
        self.client = FederatedIdentityClient()

    def start_login(self, state: str) -> str:
        return self.client.start_oauth_flow(state)


if __name__ == "__main__":
    starter = OAuthLoginStarter()
    state = "sample_state_123"
    auth_url = starter.start_login(state)
    print(f"Redirect to: {auth_url}")
