from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class IdentitySettings:
    api_base: str = os.getenv("IDENTITY_API_BASE", "https://api.clerk.com")
    secret_key: str = os.getenv("CLERK_SECRET_KEY", "")
    project_id: Optional[str] = os.getenv("IDENTITY_PROJECT_ID")


class IdentityClientError(RuntimeError):
    pass


class IdentityClient:
    def __init__(self, settings: Optional[IdentitySettings] = None) -> None:
        self.settings = settings or IdentitySettings()
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.settings.secret_key}", "Content-Type": "application/json"})

    def _request(self, method: str, path: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.settings.api_base.rstrip('/')}{path}"
        resp = self.session.request(method, url, json=json, timeout=30)
        if resp.status_code >= 400:
            raise IdentityClientError(f"{resp.status_code}: {resp.text}")
        return resp.json() if resp.content else {}

    def post(self, path: str, json: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", path, json=json)

    def get(self, path: str) -> Dict[str, Any]:
        return self._request("GET", path)


def get_identity_client() -> IdentityClient:
    return IdentityClient()
