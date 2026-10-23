import os
import base64
import json
from typing import Optional
from urllib.parse import urlencode


AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "dev-example.us.auth0.com")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET", "")
AUTH0_MANAGEMENT_API_TOKEN = os.environ.get("AUTH0_MANAGEMENT_API_TOKEN", "")
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE", f"https://{AUTH0_DOMAIN}/api/v2/")

AUTH0_BASE_URL = f"https://{AUTH0_DOMAIN}"
AUTH0_OAUTH_TOKEN_URL = f"{AUTH0_BASE_URL}/oauth/token"
AUTH0_DB_CONNECTIONS_URL = f"{AUTH0_BASE_URL}/api/v2/connections"
AUTH0_PASSWORD_CHANGE_URL = f"{AUTH0_BASE_URL}/dbconnections/change_password"
AUTH0_USER_REGISTRATION_URL = f"{AUTH0_BASE_URL}/api/v2/users"


class Auth0ClientConfig:
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
        self.base_url = f"https://{self.domain}"
        self.oauth_token_url = f"{self.base_url}/oauth/token"
        self.management_api_url = f"{self.base_url}/api/v2"
        self.db_connections_url = f"{self.base_url}/dbconnections"

    def get_management_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.management_token}",
            "Content-Type": "application/json",
        }

    def get_oauth_headers(self) -> dict:
        return {
            "Content-Type": "application/json",
        }

    def get_basic_auth_header(self) -> str:
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"


def build_auth0_api_url(path: str) -> str:
    domain = os.environ.get("AUTH0_DOMAIN", "dev-example.us.auth0.com")
    return f"https://{domain}{path}"


def build_oauth_payload(
    grant_type: str,
    client_id: str,
    client_secret: str,
    extra_params: Optional[dict] = None,
) -> dict:
    payload = {
        "grant_type": grant_type,
        "client_id": client_id,
        "client_secret": client_secret,
    }
    if extra_params:
        payload.update(extra_params)
    return payload


def parse_auth0_error(response_data: dict) -> str:
    error = response_data.get("error", "unknown_error")
    error_description = response_data.get("error_description", "An error occurred")
    return f"Auth0 error [{error}]: {error_description}"


def extract_user_id_from_auth0_response(data: dict) -> str:
    return data.get("user_id", data.get("_id", ""))


def extract_tokens_from_auth0_response(data: dict) -> dict:
    return {
        "access_token": data.get("access_token", ""),
        "id_token": data.get("id_token", ""),
        "refresh_token": data.get("refresh_token"),
        "token_type": data.get("token_type", "Bearer"),
        "expires_in": data.get("expires_in", 0),
        "scope": data.get("scope", ""),
    }
