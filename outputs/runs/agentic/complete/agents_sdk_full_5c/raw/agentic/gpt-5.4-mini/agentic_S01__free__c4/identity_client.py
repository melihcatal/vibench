from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


DEFAULT_BASE_URL = "https://identitytoolkit.googleapis.com/v1"


@dataclass(frozen=True)
class IdentityConfig:
    api_key: str
    project_id: Optional[str] = None
    base_url: str = DEFAULT_BASE_URL

    @classmethod
    def from_env(cls) -> "IdentityConfig":
        api_key = os.environ.get("FIREBASE_WEB_API_KEY") or os.environ.get("GOOGLE_CLOUD_API_KEY")
        if not api_key:
            raise RuntimeError("Missing FIREBASE_WEB_API_KEY or GOOGLE_CLOUD_API_KEY")
        return cls(
            api_key=api_key,
            project_id=os.environ.get("FIREBASE_PROJECT_ID"),
            base_url=os.environ.get("FIREBASE_IDENTITY_BASE_URL", DEFAULT_BASE_URL),
        )


class IdentityClient:
    def __init__(self, config: Optional[IdentityConfig] = None, session: Optional[requests.Session] = None):
        self.config = config or IdentityConfig.from_env()
        self.session = session or requests.Session()

    def endpoint(self, path: str) -> str:
        return f"{self.config.base_url.rstrip('/')}/{path.lstrip('/')}?key={self.config.api_key}"

    def post(self, path: str, json: Dict[str, Any]) -> Dict[str, Any]:
        response = self.session.post(self.endpoint(path), json=json, timeout=30)
        response.raise_for_status()
        return response.json()
