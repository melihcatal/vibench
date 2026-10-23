import os
from dataclasses import dataclass


@dataclass
class OAuthConfig:
    client_id: str
    client_secret: str | None  # Optional for public clients (PKCE)
    redirect_uri: str
    scope: list[str]
    issuer_url: str | None = None  # For OIDC discovery


class IdentityClients:
    """
    Centralized configuration for various identity providers.
    """

    @staticmethod
    def get_google_config() -> OAuthConfig:
        return OAuthConfig(
            client_id=os.environ.get("GOOGLE_CLIENT_ID", ""),
            client_secret=os.environ.get("GOOGLE_CLIENT_SECRET", ""),
            redirect_uri=os.environ.get(
                "GOOGLE_REDIRECT_URI", "http://localhost:8080/oauth/callback/google"
            ),
            scope=["openid", "email", "profile"],
            issuer_url="https://accounts.google.com",
        )

    @staticmethod
    def get_auth0_config() -> OAuthConfig:
        return OAuthConfig(
            client_id=os.environ.get("AUTH0_CLIENT_ID", ""),
            client_secret=os.environ.get(
                "AUTH0_CLIENT_SECRET", None
            ),  # Auth0 PKCE typically doesn't use client_secret on client-side
            redirect_uri=os.environ.get(
                "AUTH0_REDIRECT_URI", "http://localhost:8080/auth0/callback"
            ),
            scope=["openid", "profile", "email"],
            issuer_url=f"https://{os.environ.get('AUTH0_DOMAIN', 'YOUR_AUTH0_DOMAIN.auth0.com')}",
        )


# Example usage (for demonstration, in a real app these would be imported and used)
if __name__ == "__main__":
    google_cfg = IdentityClients.get_google_config()
    print(f"Google Client ID: {google_cfg.client_id}")
    print(f"Google Redirect URI: {google_cfg.redirect_uri}")

    auth0_cfg = IdentityClients.get_auth0_config()
    print(f"Auth0 Client ID: {auth0_cfg.client_id}")
    print(f"Auth0 Issuer URL: {auth0_cfg.issuer_url}")
