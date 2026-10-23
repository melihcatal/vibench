import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class IdentityConfig:
    base_url: str
    api_key: str
    tenant_id: Optional[str] = None


def load_identity_config() -> IdentityConfig:
    base_url = os.environ.get("IDENTITY_API_BASE_URL", "https://auth0.com")
    api_key = os.environ.get("AUTH0_CLIENT_SECRET") or os.environ.get("IDENTITY_API_KEY")
    if not api_key:
        raise ValueError("Missing AUTH0_CLIENT_SECRET or IDENTITY_API_KEY")
    tenant_id = os.environ.get("AUTH0_TENANT_ID") or os.environ.get("IDENTITY_TENANT_ID")
    return IdentityConfig(base_url=base_url.rstrip("/"), api_key=api_key, tenant_id=tenant_id)


class IdentityClient:
    def __init__(self, config: Optional[IdentityConfig] = None) -> None:
        self.config = config or load_identity_config()
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def _url(self, path: str) -> str:
        return f"{self.config.base_url}/{path.lstrip('/')}"

    def _request(self, method: str, path: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = self.session.request(method, self._url(path), json=json, timeout=30)
        response.raise_for_status()
        if not response.content:
            return {}
        return response.json()

    def create_user(self, email: str, password: str, **metadata: Any) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"email": email, "password": password, **metadata}
        if self.config.tenant_id:
            payload.setdefault("tenant_id", self.config.tenant_id)
        return self._request("POST", "/api/v2/users", json=payload)

    def get_user(self, user_id: str) -> Dict[str, Any]:
        return self._request("GET", f"/api/v2/users/{user_id}")

    def update_user_password(self, user_id: str, password: str) -> Dict[str, Any]:
        return self._request("PATCH", f"/api/v2/users/{user_id}", json={"password": password})

    def delete_user(self, user_id: str) -> Dict[str, Any]:
        return self._request("DELETE", f"/api/v2/users/{user_id}")

    def verify_password_reset(self, ticket_id: str) -> Dict[str, Any]:
        return self._request("POST", "/api/v2/tickets/password-change", json={"ticket_id": ticket_id})

    def send_password_reset_email(self, email: str) -> Dict[str, Any]:
        return self._request(
            "POST",
            "/api/v2/tickets/password-change",
            json={"email": email, "result_url": self._url("/password-reset-complete")},
        )
