import os
from auth0.authentication import Auth0


class IdentityClient:
    def __init__(self):
        self.domain = os.environ.get("AUTH0_DOMAIN")
        self.client_id = os.environ.get("AUTH0_CLIENT_ID")
        self.client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
        self.callback_url = os.environ.get(
            "AUTH0_CALLBACK_URL", "http://localhost:3000/callback"
        )

        if not all([self.domain, self.client_id, self.client_secret]):
            raise ValueError(
                "AUTH0_DOMAIN, AUTH0_CLIENT_ID, and AUTH0_CLIENT_SECRET must be set"
            )

        self.auth0 = Auth0(
            self.domain, self.client_id, client_secret=self.client_secret
        )


def get_identity_client() -> IdentityClient:
    return IdentityClient()
