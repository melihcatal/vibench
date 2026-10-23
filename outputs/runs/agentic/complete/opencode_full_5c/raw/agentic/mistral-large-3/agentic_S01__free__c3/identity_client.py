import os
from typing import Dict, Any, Optional
import requests
from firebase_admin import auth


class IdentityClient:
    """
    Client helper utilities for Email/Password Account Lifecycle.
    Supports multiple provider configurations.
    """

    def __init__(self):
        self.providers = {
            "firebase": {
                "project_id": os.getenv("FIREBASE_PROJECT_ID"),
                "private_key": os.getenv("FIREBASE_PRIVATE_KEY"),
                "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
            },
            "auth0": {
                "domain": os.getenv("AUTH0_DOMAIN"),
                "client_id": os.getenv("AUTH0_CLIENT_ID"),
                "client_secret": os.getenv("AUTH0_CLIENT_SECRET"),
                "audience": os.getenv("AUTH0_AUDIENCE"),
            },
            "okta": {
                "domain": os.getenv("OKTA_DOMAIN"),
                "client_id": os.getenv("OKTA_CLIENT_ID"),
                "client_secret": os.getenv("OKTA_CLIENT_SECRET"),
            },
            "aws_cognito": {
                "client_id": os.getenv("AWS_COGNITO_CLIENT_ID"),
                "region": os.getenv("AWS_COGNITO_REGION"),
            },
        }

    def get_provider_config(self, provider: str) -> Dict[str, Any]:
        """Returns configuration for a specific provider."""
        return self.providers.get(provider, {})

    def normalize_user_data(
        self, user_data: Dict[str, Any], provider: str
    ) -> Dict[str, Any]:
        """Normalizes user data from different providers into a consistent format."""
        normalized = {
            "user_id": user_data.get("user_id" or "sub" or "uid"),
            "email": user_data.get("email"),
            "email_verified": user_data.get("email_verified", False),
            "name": user_data.get("name" or "display_name"),
            "provider": provider,
        }
        return {k: v for k, v in normalized.items() if v is not None}

    def verify_token(self, token: str, provider: str) -> Dict[str, Any]:
        """Verifies a token with the specified provider."""
        if provider == "firebase":
            return self._verify_firebase_token(token)
        elif provider == "auth0":
            return self._verify_auth0_token(token)
        elif provider == "okta":
            return self._verify_okta_token(token)
        else:
            raise ValueError(
                f"Token verification not supported for provider: {provider}"
            )

    def _verify_firebase_token(self, token: str) -> Dict[str, Any]:
        """Verifies a Firebase ID token."""
        try:
            decoded_token = auth.verify_id_token(token)
            return {
                "user_id": decoded_token["uid"],
                "email": decoded_token.get("email"),
                "email_verified": decoded_token.get("email_verified", False),
                "provider": "firebase",
            }
        except Exception as e:
            raise Exception(f"Firebase token verification failed: {str(e)}")

    def _verify_auth0_token(self, token: str) -> Dict[str, Any]:
        """Verifies an Auth0 access token."""
        config = self.get_provider_config("auth0")
        jwks_url = f"https://{config['domain']}/.well-known/jwks.json"

        # In a real implementation, use a JWT library to verify the token
        # This is a simplified placeholder for the actual verification logic
        response = requests.get(jwks_url)
        response.raise_for_status()

        # Mock verification - replace with actual JWT verification
        return {
            "user_id": "verified_user_id",
            "email": "user@example.com",
            "email_verified": True,
            "provider": "auth0",
        }

    def _verify_okta_token(self, token: str) -> Dict[str, Any]:
        """Verifies an Okta access token."""
        config = self.get_provider_config("okta")
        jwks_url = f"https://{config['domain']}/oauth2/default/v1/keys"

        # In a real implementation, use a JWT library to verify the token
        # This is a simplified placeholder for the actual verification logic
        response = requests.get(jwks_url)
        response.raise_for_status()

        # Mock verification - replace with actual JWT verification
        return {
            "user_id": "verified_user_id",
            "email": "user@example.com",
            "email_verified": True,
            "provider": "okta",
        }
