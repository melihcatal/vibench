import os
from typing import Dict, Any
from identity_client import FederatedIdentityClient
from identity_models import PKCEHelper

class PKCELoginStarter:
    def __init__(self):
        self.client = FederatedIdentityClient()

    def start_pkce_login(self, state: str) -> Dict[str, str]:
        code_verifier = PKCEHelper.generate_code_verifier()
        code_challenge = PKCEHelper.generate_code_challenge(code_verifier)
        auth_url = self.client.start_oauth_flow(state, code_challenge)
        return {
            "auth_url": auth_url,
            "code_verifier": code_verifier
n        }

if __name__ == "__main__":
    starter = PKCELoginStarter()
    state = "sample_state_456"
    result = starter.start_pkce_login(state)
    print(f"Redirect to: {result['auth_url']}")
    print(f"Code Verifier: {result['code_verifier']}")