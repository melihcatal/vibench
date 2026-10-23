from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests
from google.cloud import firestore


FIREBASE_WEB_API_KEY_ENV = "FIREBASE_WEB_API_KEY"
FIREBASE_PROJECT_ID_ENV = "FIREBASE_PROJECT_ID"
GOOGLE_APPLICATION_CREDENTIALS_ENV = "GOOGLE_APPLICATION_CREDENTIALS"

IDENTITY_TOOLKIT_BASE_URL = "https://identitytoolkit.googleapis.com/v1"
SECURE_TOKEN_BASE_URL = "https://securetoken.googleapis.com/v1"


class IdentityConfigurationError(RuntimeError):
    pass


class IdentityAPIError(RuntimeError):
    def __init__(self, message: str, *, status_code: Optional[int] = None, payload: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload or {}



def get_firebase_web_api_key() -> str:
    api_key = os.getenv(FIREBASE_WEB_API_KEY_ENV)
    if not api_key:
        raise IdentityConfigurationError(f"Missing required environment variable: {FIREBASE_WEB_API_KEY_ENV}")
    return api_key



def get_firebase_project_id() -> str:
    project_id = os.getenv(FIREBASE_PROJECT_ID_ENV)
    if not project_id:
        raise IdentityConfigurationError(f"Missing required environment variable: {FIREBASE_PROJECT_ID_ENV}")
    return project_id



def identity_toolkit_url(method_name: str) -> str:
    return f"{IDENTITY_TOOLKIT_BASE_URL}/accounts:{method_name}?key={get_firebase_web_api_key()}"



def secure_token_url() -> str:
    return f"{SECURE_TOKEN_BASE_URL}/token?key={get_firebase_web_api_key()}"



def post_json(url: str, payload: Dict[str, Any], *, timeout: int = 30) -> Dict[str, Any]:
    response = requests.post(url, json=payload, timeout=timeout)
    try:
        data = response.json()
    except ValueError:
        data = {"raw_text": response.text}
    if not response.ok:
        message = data.get("error", {}).get("message") if isinstance(data, dict) else None
        raise IdentityAPIError(message or "Firebase Identity Toolkit request failed", status_code=response.status_code, payload=data)
    return data



def post_form(url: str, payload: Dict[str, Any], *, timeout: int = 30) -> Dict[str, Any]:
    response = requests.post(url, data=payload, timeout=timeout)
    try:
        data = response.json()
    except ValueError:
        data = {"raw_text": response.text}
    if not response.ok:
        message = data.get("error", {}).get("message") if isinstance(data, dict) else None
        raise IdentityAPIError(message or "Google Secure Token request failed", status_code=response.status_code, payload=data)
    return data



def get_firestore_client() -> firestore.Client:
    return firestore.Client(project=get_firebase_project_id())
