import os
from auth0.management import Auth0
from auth0.authentication import Auth0Authentication


class IdentityClient:
    def __init__(self):
        self.domain = os.environ.get("AUTH0_DOMAIN")
        self.management_client_id = os.environ.get("AUTH0_MANAGEMENT_CLIENT_ID")
        self.management_client_secret = os.environ.get("AUTH0_MANAGEMENT_CLIENT_SECRET")
        self.authentication_client_id = os.environ.get("AUTH0_AUTHENTICATION_CLIENT_ID")
        self.authentication_client_secret = os.environ.get(
            "AUTH0_AUTHENTICATION_CLIENT_SECRET"
        )

        if not all(
            [
                self.domain,
                self.management_client_id,
                self.management_client_secret,
                self.authentication_client_id,
                self.authentication_client_secret,
            ]
        ):
            raise ValueError(
                "Auth0 environment variables not set. Please set AUTH0_DOMAIN, AUTH0_MANAGEMENT_CLIENT_ID, AUTH0_MANAGEMENT_CLIENT_SECRET, AUTH0_AUTHENTICATION_CLIENT_ID, AUTH0_AUTHENTICATION_CLIENT_SECRET."
            )

        self.management_client = Auth0(
            self.domain, self.management_client_id, self.management_client_secret
        )
        self.authentication_client = Auth0Authentication(
            self.domain, self.authentication_client_id
        )
