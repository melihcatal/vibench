import os
from typing import Dict, Any


class Auth0ClientConfig:
    """
    Provides configuration for Auth0 client.
    """

    def __init__(self):
        self.domain = os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN.auth0.com")
        self.client_id = os.environ.get("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID")
        self.client_secret = os.environ.get(
            "AUTH0_CLIENT_SECRET", "YOUR_AUTH0_CLIENT_SECRET"
        )
        self.callback_url = os.environ.get(
            "AUTH0_CALLBACK_URL", "http://localhost:8000/callback"
        )
        self.pkce_client_id = os.environ.get(
            "AUTH0_CLIENT_ID_FOR_PKCE", "YOUR_AUTH0_CLIENT_ID_FOR_PKCE"
        )

    def get_token_endpoint(self) -> str:
        return f"https://{self.domain}/oauth/token"

    def get_authorize_endpoint(self) -> str:
        return f"https://{self.domain}/authorize"

    def get_userinfo_endpoint(self) -> str:
        return f"https://{self.domain}/userinfo"


def get_auth0_config() -> Auth0ClientConfig:
    return Auth0ClientConfig()


# Example of a generic utility function for making requests (could be expanded)
def make_request(
    method: str, url: str, headers: Dict[str, str] = None, json: Dict[str, Any] = None
) -> Dict[str, Any]:
    import requests

    try:
        if method.lower() == "post":
            response = requests.post(url, headers=headers, json=json)
        elif method.lower() == "get":
            response = requests.get(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return {"error": str(e)}
