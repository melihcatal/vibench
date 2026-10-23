import os
import requests
from auth0.management import Auth0
from auth0.authentication import Auth0Authentication


class Auth0Client:
    def __init__(self):
        self.domain = os.environ.get("AUTH0_DOMAIN")
        if not self.domain:
            raise ValueError("AUTH0_DOMAIN environment variable not set.")

        # Management API Client
        management_client_id = os.environ.get("AUTH0_MANAGEMENT_CLIENT_ID")
        management_client_secret = os.environ.get("AUTH0_MANAGEMENT_CLIENT_SECRET")
        if not management_client_id or not management_client_secret:
            raise ValueError(
                "AUTH0_MANAGEMENT_CLIENT_ID or AUTH0_MANAGEMENT_CLIENT_SECRET environment variable not set."
            )

        # To get a management API token, first need to get a token using client_credentials grant type
        token_url = f"https://{self.domain}/oauth/token"
        payload = {
            "client_id": management_client_id,
            "client_secret": management_client_secret,
            "audience": f"https://{self.domain}/api/v2/",
            "grant_type": "client_credentials",
        }
        response = requests.post(token_url, json=payload)
        response.raise_for_status()
        management_api_token = response.json().get("access_token")

        self.management_client = Auth0(self.domain, management_api_token)

        # Authentication API Client (for direct login/refresh/reset)
        self.client_id = os.environ.get("AUTH0_CLIENT_ID")
        self.client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
        if not self.client_id or not self.client_secret:
            raise ValueError(
                "AUTH0_CLIENT_ID or AUTH0_CLIENT_SECRET environment variable not set."
            )

        self.authentication_url = f"https://{self.domain}/oauth/token"
        self.password_reset_url = f"https://{self.domain}/dbconnections/change_password"


auth0_client = Auth0Client()
