import os

class IdentityClientConfig:
    """Centralized configuration for Auth0 identity client."""
    AUTH0_DOMAIN: str = os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN")
    AUTH0_CLIENT_ID: str = os.environ.get("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET: str = os.environ.get("AUTH0_CLIENT_SECRET", "YOUR_AUTH0_CLIENT_SECRET")
    AUTH0_CALLBACK_URL: str = os.environ.get("AUTH0_CALLBACK_URL", "http://localhost:8000/callback")

    def __repr__(self):
        # Mask sensitive info for representation
        return (
            f"IdentityClientConfig(domain='{self.AUTH0_DOMAIN}', "
            f"client_id='{self.AUTH0_CLIENT_ID}', "
            f"client_secret='********', " # Masked
            f"callback_url='{self.AUTH0_CALLBACK_URL}')"
        )


class Auth0ClientHelper:
    """Helper utilities for interacting with Auth0."""

    @staticmethod
    def get_auth_url(domain: str, client_id: str, redirect_uri: str, scope: str = "openid profile email") -> str:
        from urllib.parse import quote_plus, urlencode
        return (
            f"https://{domain}/authorize?"
            + urlencode(
                {
                    "scope": scope,
                    "response_type": "code",
                    "client_id": client_id,
                    "redirect_uri": redirect_uri,
                },
                quote_via=quote_plus,
            )
        )

    @staticmethod
    def get_token_url(domain: str) -> str:
        return f"https://{domain}/oauth/token"

    @staticmethod
    def get_userinfo_url(domain: str) -> str:
        return f"https://{domain}/userinfo"
