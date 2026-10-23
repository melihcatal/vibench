import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class IdentityConfig:
    api_base_url: str
    api_key: Optional[str] = None
    tenant_id: Optional[str] = None


def load_identity_config() -> IdentityConfig:
    return IdentityConfig(
        api_base_url=os.getenv("IDENTITY_API_BASE_URL", "https://api.identitytoolkit.googleapis.com/v1"),
        api_key=os.getenv("FIREBASE_WEB_API_KEY"),
        tenant_id=os.getenv("FIREBASE_TENANT_ID"),
    )


class IdentityClient:
    def __init__(self, config: Optional[IdentityConfig] = None) -> None:
        self.config = config or load_identity_config()
        self.session = requests.Session()

    def _params(self) -> Dict[str, str]:
        params: Dict[str, str] = {}
        if self.config.api_key:
            params["key"] = self.config.api_key
        if self.config.tenant_id:
            params["tenantId"] = self.config.tenant_id
        return params

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self.session.post(
            f"{self.config.api_base_url.rstrip('/')}/{path.lstrip('/')}",
            params=self._params(),
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def sign_up(self, email: str, password: str) -> Dict[str, Any]:
        return self._post("accounts:signUp", {"email": email, "password": password, "returnSecureToken": True})

    def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        return self._post("accounts:signInWithPassword", {"email": email, "password": password, "returnSecureToken": True})

    def send_password_reset_email(self, email: str) -> Dict[str, Any]:
        return self._post("accounts:sendOobCode", {"requestType": "PASSWORD_RESET", "email": email})

    def change_password(self, id_token: str, new_password: str) -> Dict[str, Any]:
        return self._post("accounts:update", {"idToken": id_token, "password": new_password, "returnSecureToken": True})

    def delete_account(self, id_token: str) -> Dict[str, Any]:
        return self._post("accounts:delete", {"idToken": id_token})
