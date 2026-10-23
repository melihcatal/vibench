import os


class IdentityClient:
    """Local helper configuring a concrete identity provider (Auth0) and providing client utilities."""

    def __init__(self):
        # In production these would be loaded from env vars or a secrets manager
        self.client_id = os.getenv("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID")
        self.client_secret = os.getenv(
            "AUTH0_CLIENT_SECRET", "YOUR_AUTH0_CLIENT_SECRET"
        )
        self.redirect_uri = os.getenv(
            "AUTH0_REDIRECT_URI", "http://localhost:3000/callback"
        )
        self.audience = os.getenv("AUTH0_AUDIENCE", "https://your_api_identifier")

    def client_info(self):
        return {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "audience": self.audience,
        }
