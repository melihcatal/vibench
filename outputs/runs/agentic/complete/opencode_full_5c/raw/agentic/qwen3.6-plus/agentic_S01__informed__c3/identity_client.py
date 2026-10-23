import os
from typing import Optional, Dict, Any
import requests


AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET", "")
AUTH0_MANAGEMENT_API_TOKEN = os.environ.get("AUTH0_MANAGEMENT_API_TOKEN", "")
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE", "")

AUTH0_BASE_URL = f"https://{AUTH0_DOMAIN}" if AUTH0_DOMAIN else ""
AUTH0_OAUTH_TOKEN_URL = f"{AUTH0_BASE_URL}/oauth/token"
AUTH0_DB_CONNECTIONS_URL = f"{AUTH0_BASE_URL}/api/v2/users-by-email"
AUTH0_PASSWORD_CHANGE_URL = f"{AUTH0_BASE_URL}/dbconnections/change_password"


class IdentityConfig:
    def __init__(
        self,
        domain: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        management_token: Optional[str] = None,
        audience: Optional[str] = None,
    ):
        self.domain = domain or AUTH0_DOMAIN
        self.client_id = client_id or AUTH0_CLIENT_ID
        self.client_secret = client_secret or AUTH0_CLIENT_SECRET
        self.management_token = management_token or AUTH0_MANAGEMENT_API_TOKEN
        self.audience = audience or AUTH0_AUDIENCE
        self.base_url = f"https://{self.domain}" if self.domain else ""

    def get_oauth_token_url(self) -> str:
        return f"{self.base_url}/oauth/token"

    def get_db_connection_change_password_url(self) -> str:
        return f"{self.base_url}/dbconnections/change_password"

    def get_users_by_email_url(self) -> str:
        return f"{self.base_url}/api/v2/users-by-email"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "domain": self.domain,
            "client_id": self.client_id,
            "audience": self.audience,
        }


class Auth0APIClient:
    def __init__(self, config: Optional[IdentityConfig] = None):
        self.config = config or IdentityConfig()
        self.session = requests.Session()

    def _get_management_headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
        }
        if self.config.management_token:
            headers["Authorization"] = f"Bearer {self.config.management_token}"
        return headers

    def _get_oauth_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
        }

    def post(
        self,
        url: str,
        payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        resp = self.session.post(
            url, json=payload, headers=headers or self._get_oauth_headers()
        )
        return resp

    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        resp = self.session.get(
            url, params=params, headers=headers or self._get_oauth_headers()
        )
        return resp

    def get_management_token(self) -> Optional[str]:
        return self.config.management_token

    def close(self):
        self.session.close()


def load_identity_config() -> IdentityConfig:
    return IdentityConfig(
        domain=os.environ.get("AUTH0_DOMAIN"),
        client_id=os.environ.get("AUTH0_CLIENT_ID"),
        client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
        management_token=os.environ.get("AUTH0_MANAGEMENT_API_TOKEN"),
        audience=os.environ.get("AUTH0_AUDIENCE"),
    )


def create_auth0_client(config: Optional[IdentityConfig] = None) -> Auth0APIClient:
    return Auth0APIClient(config=config)
