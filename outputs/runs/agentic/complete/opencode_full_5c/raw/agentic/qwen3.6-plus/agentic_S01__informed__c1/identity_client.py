import os
from typing import Optional, Dict, Any, Tuple
import requests
from identity_models import (
    RegisterUserRequest,
    LoginRequest,
    RefreshTokenRequest,
    PasswordResetRequest,
    TokenResponse,
    UserResponse,
    PasswordResetResponse,
)


class Auth0Config:
    def __init__(
        self,
        domain: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        audience: Optional[str] = None,
    ):
        self.domain = domain or os.environ.get("AUTH0_DOMAIN", "")
        self.client_id = client_id or os.environ.get("AUTH0_CLIENT_ID", "")
        self.client_secret = client_secret or os.environ.get("AUTH0_CLIENT_SECRET", "")
        self.audience = audience or os.environ.get("AUTH0_AUDIENCE", "")
        self.management_audience = os.environ.get(
            "AUTH0_MANAGEMENT_AUDIENCE", f"https://{self.domain}/api/v2/"
        )

        if not self.domain:
            raise ValueError("AUTH0_DOMAIN environment variable is required")
        if not self.client_id:
            raise ValueError("AUTH0_CLIENT_ID environment variable is required")
        if not self.client_secret:
            raise ValueError("AUTH0_CLIENT_SECRET environment variable is required")

    @property
    def base_url(self) -> str:
        return f"https://{self.domain}"

    @property
    def oauth_token_url(self) -> str:
        return f"{self.base_url}/oauth/token"

    @property
    def db_connections_url(self) -> str:
        return f"{self.base_url}/dbconnections"

    @property
    def management_base_url(self) -> str:
        return f"{self.base_url}/api/v2"


class IdentityClient:
    def __init__(self, config: Optional[Auth0Config] = None):
        self.config = config or Auth0Config()
        self._management_token: Optional[str] = None

    def _get_management_token(self) -> str:
        if self._management_token:
            return self._management_token

        payload = {
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "audience": self.config.management_audience,
            "grant_type": "client_credentials",
        }

        response = requests.post(self.config.oauth_token_url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        self._management_token = data["access_token"]
        return self._management_token

    def _management_headers(self) -> Dict[str, str]:
        token = self._get_management_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def register_user(self, request: RegisterUserRequest) -> UserResponse:
        payload = request.to_auth0_payload()
        url = f"{self.config.db_connections_url}/signup"
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return UserResponse.from_auth0_response(response.json())

    def login(self, request: LoginRequest) -> TokenResponse:
        payload = request.to_auth0_payload()
        if self.config.audience and not payload.get("audience"):
            payload["audience"] = self.config.audience
        response = requests.post(self.config.oauth_token_url, json=payload, timeout=30)
        response.raise_for_status()
        return TokenResponse.from_auth0_response(response.json())

    def refresh_session(self, request: RefreshTokenRequest) -> TokenResponse:
        payload = request.to_auth0_payload()
        data = {
            "grant_type": "refresh_token",
            "refresh_token": request.refresh_token,
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
        }
        if request.scope:
            data["scope"] = request.scope
        if request.audience or self.config.audience:
            data["audience"] = request.audience or self.config.audience

        response = requests.post(self.config.oauth_token_url, json=data, timeout=30)
        response.raise_for_status()
        return TokenResponse.from_auth0_response(response.json())

    def initiate_password_reset(
        self, request: PasswordResetRequest
    ) -> PasswordResetResponse:
        payload = request.to_auth0_payload()
        if not payload.get("client_id"):
            payload["client_id"] = self.config.client_id

        url = f"{self.config.management_base_url}/tickets/password-change"
        headers = self._management_headers()
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return PasswordResetResponse.from_auth0_response(response.json(), request.email)

    def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        url = f"{self.config.management_base_url}/users-by-email"
        headers = self._management_headers()
        params = {"email": email}
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        results = response.json()
        if results:
            return UserResponse.from_auth0_response(results[0])
        return None
