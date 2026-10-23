import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class IdentityClient:
    domain: str = os.getenv("AUTH0_DOMAIN", "")
    client_id: str = os.getenv("AUTH0_CLIENT_ID", "")
    client_secret: str = os.getenv("AUTH0_CLIENT_SECRET", "")
    audience: str = os.getenv("AUTH0_AUDIENCE", "")

    @property
    def auth0(self) -> "Auth0Client":
        return Auth0Client(self.domain, self.client_id, self.client_secret, self.audience)


class Auth0Client:
    def __init__(self, domain: str, client_id: str, client_secret: str, audience: str):
        self.domain = domain.rstrip("/")
        self.client_id = client_id
        self.client_secret = client_secret
        self.audience = audience

    def signup_email_password(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._post("https://{}/dbconnections/signup".format(self.domain), payload)

    def login_email_password(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._post("https://{}/oauth/token".format(self.domain), payload)

    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        payload = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": refresh_token,
        }
        if self.client_secret:
            payload["client_secret"] = self.client_secret
        return self._post("https://{}/oauth/token".format(self.domain), payload)

    def request_password_reset(self, email: str) -> Dict[str, Any]:
        payload = {"client_id": self.client_id, "email": email, "connection": "Username-Password-Authentication"}
        return self._post("https://{}/dbconnections/change_password".format(self.domain), payload)

    def _post(self, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            return {"raw": response.text}


def build_user_payload(request: Any) -> Dict[str, Any]:
    return {"email": request.email, "password": request.password, "connection": "Username-Password-Authentication"}


def build_login_payload(request: Any) -> Dict[str, Any]:
    return {
        "grant_type": "password",
        "username": request.email,
        "password": request.password,
        "client_id": os.getenv("AUTH0_CLIENT_ID", ""),
        "client_secret": os.getenv("AUTH0_CLIENT_SECRET", ""),
        "audience": os.getenv("AUTH0_AUDIENCE", ""),
        "scope": "openid profile email offline_access",
    }


def normalize_auth_result(response: Dict[str, Any], email: str) -> Any:
    from identity_models import AuthResult
    return AuthResult(email=email, access_token=response.get("access_token", ""), refresh_token=response.get("refresh_token", ""), id_token=response.get("id_token", ""), raw=response)


def normalize_refresh_result(response: Dict[str, Any]) -> Any:
    from identity_models import RefreshResponse
    return RefreshResponse(access_token=response.get("access_token", ""), refresh_token=response.get("refresh_token", ""), id_token=response.get("id_token", ""), raw=response)
