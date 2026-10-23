import os
from typing import Dict, Any, Tuple
import boto3
import requests


class IdentityClient:
    """
    Central helper for all federated login steps.
    The concrete provider in this file is Amazon Cognito federation.
    Reference: service=Amazon Cognito federation; interface=sdk_or_protocol
    """

    def __init__(
        self,
        provider: str,
        domain: str,
        client_id: str,
        client_secret: str = None,
        redirect_uri: str = None,
    ):
        self.provider = provider
        self.domain = domain
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        # Cognito specific client for token exchange and user pool data
        self.cognito_client = boto3.client(
            "cognito-idp", region_name=os.getenv("AWS_REGION", "us-east-1")
        )

    def exchange_code_for_tokens(self, auth_code: str) -> Dict[str, str]:
        """Exchange authorization code for access/refresh/id tokens."""
        response = self.cognito_client.initiate_auth(
            AuthFlow="AUTH_CODE_GRANT",  # Use GRANT flow for code exchange
            ClientId=self.client_id,
            AuthParameters={
                "code": auth_code,
                "redirect_uri": self.redirect_uri,
                "client_id": self.client_id,
            },
            ClientMetadata={},
        )
        return response[
            "AuthenticationResult"
        ]  # contains id_token, access_token, refresh_token

    def fetch_user_profile(self, id_token: str) -> Dict[str, Any]:
        """Retrieve and normalize user profile claims from id_token."""
        # Cognito does not expose a separate user info endpoint; decode id_token locally.
        # For demo we just decode JWT header/payload (using PyJWT could be added).
        # Here we return a placeholder dict.
        fake_profile = {
            "sub": "1234567890",
            "email": "user@example.com",
            "email_verified": True,
            "preferred_username": "jdoe",
            "name": "John Doe",
            "family_name": "Doe",
            "given_name": "John",
        }
        return fake_profile

    def logout(self):
        """Optional: perform logout (revoke tokens)."""
        # Cognito does not have a public revoke endpoint; token revocation can be handled client-side.
        pass
