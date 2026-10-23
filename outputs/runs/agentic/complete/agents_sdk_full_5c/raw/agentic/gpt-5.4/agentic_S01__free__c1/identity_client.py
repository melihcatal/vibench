from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


class IdentityClientError(RuntimeError):
    pass


class FirebaseIdentityToolkitClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        session: Optional[requests.Session] = None,
        timeout: int = 30,
    ) -> None:
        self.api_key = api_key or os.environ["FIREBASE_WEB_API_KEY"]
        self.session = session or requests.Session()
        self.timeout = timeout
        self.identity_base_url = "https://identitytoolkit.googleapis.com/v1"
        self.secure_token_url = "https://securetoken.googleapis.com/v1/token"

    def _request_json(self, method: str, url: str, *, params: Optional[Dict[str, Any]] = None, json_body: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json_body,
            data=data,
            timeout=self.timeout,
        )
        if not response.ok:
            try:
                detail = response.json()
            except ValueError:
                detail = {"error": {"message": response.text}}
            raise IdentityClientError(str(detail))
        return response.json()

    def sign_up(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request_json(
            "POST",
            f"{self.identity_base_url}/accounts:signUp",
            params={"key": self.api_key},
            json_body=payload,
        )

    def sign_in_with_password(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request_json(
            "POST",
            f"{self.identity_base_url}/accounts:signInWithPassword",
            params={"key": self.api_key},
            json_body=payload,
        )

    def send_oob_code(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request_json(
            "POST",
            f"{self.identity_base_url}/accounts:sendOobCode",
            params={"key": self.api_key},
            json_body=payload,
        )

    def refresh_token(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        form_payload = {**payload, "key": self.api_key}
        return self._request_json(
            "POST",
            self.secure_token_url,
            data=form_payload,
        )


def load_google_cloud_project() -> str:
    return os.environ["GOOGLE_CLOUD_PROJECT"]


def load_openai_api_key() -> str:
    return os.environ["OPENAI_API_KEY"]


def load_firestore_collection() -> str:
    return os.environ.get("FIRESTORE_ONBOARDING_COLLECTION", "onboarding_notes")
