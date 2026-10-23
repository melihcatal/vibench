import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


DEFAULT_API_BASE_URL = "https://identitytoolkit.googleapis.com/v1"


@dataclass(frozen=True)
class IdentityConfig:
    api_key: str
    api_base_url: str = DEFAULT_API_BASE_URL

    @classmethod
    def from_env(cls) -> "IdentityConfig":
        api_key = os.getenv("FIREBASE_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Missing FIREBASE_API_KEY or GOOGLE_API_KEY")
        api_base_url = os.getenv("FIREBASE_IDENTITY_BASE_URL", DEFAULT_API_BASE_URL)
        return cls(api_key=api_key, api_base_url=api_base_url.rstrip("/"))


class IdentityClientError(RuntimeError):
    pass


class IdentityClient:
    def __init__(self, config: Optional[IdentityConfig] = None) -> None:
        self.config = config or IdentityConfig.from_env()
        self.session = requests.Session()

    def _request(self, method: str, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.config.api_base_url}/{path.lstrip('/')}?key={self.config.api_key}"
        response = self.session.request(method, url, json=payload, timeout=30)
        data = response.json() if response.content else {}
        if not response.ok:
            message = data.get("error", {}).get("message") if isinstance(data, dict) else None
            raise IdentityClientError(message or f"Request failed with status {response.status_code}")
        return data

    def sign_up(self, email: str, password: str, return_secure_token: bool = True) -> Dict[str, Any]:
        return self._request(
            "POST",
            "accounts:signUp",
            {"email": email, "password": password, "returnSecureToken": return_secure_token},
        )

    def sign_in(self, email: str, password: str, return_secure_token: bool = True) -> Dict[str, Any]:
        return self._request(
            "POST",
            "accounts:signInWithPassword",
            {"email": email, "password": password, "returnSecureToken": return_secure_token},
        )

    def send_password_reset(self, email: str) -> Dict[str, Any]:
        return self._request("POST", "accounts:sendOobCode", {"requestType": "PASSWORD_RESET", "email": email})

    def update_password(self, id_token: str, password: str) -> Dict[str, Any]:
        return self._request("POST", "accounts:update", {"idToken": id_token, "password": password, "returnSecureToken": True})

    def delete_account(self, id_token: str) -> Dict[str, Any]:
        return self._request("POST", "accounts:delete", {"idToken": id_token})


def load_identity_client() -> IdentityClient:
    return IdentityClient()


def identity_config_from_json(config_json: str) -> IdentityConfig:
    data = json.loads(config_json)
    api_key = data.get("api_key") or data.get("apiKey")
    if not api_key:
        raise ValueError("config_json must include api_key")
    api_base_url = data.get("api_base_url") or data.get("apiBaseUrl") or DEFAULT_API_BASE_URL
    return IdentityConfig(api_key=api_key, api_base_url=str(api_base_url).rstrip("/"))
