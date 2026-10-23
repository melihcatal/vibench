import json
import os
from typing import Any, Dict, Optional

import requests


class IdentityConfigurationError(RuntimeError):
    pass


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise IdentityConfigurationError(f"Missing environment variable: {name}")
    return value


def _json_headers(extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if extra:
        headers.update(extra)
    return headers


def supabase_base_url() -> str:
    return _require_env("SUPABASE_URL").rstrip("/")


def supabase_anon_key() -> str:
    return _require_env("SUPABASE_ANON_KEY")


def supabase_service_key() -> str:
    return os.getenv("SUPABASE_SERVICE_ROLE_KEY") or supabase_anon_key()


def supabase_request(
    method: str,
    path: str,
    payload: Optional[Dict[str, Any]] = None,
    use_service_role: bool = False,
) -> Dict[str, Any]:
    api_key = supabase_service_key() if use_service_role else supabase_anon_key()
    response = requests.request(
        method=method,
        url=f"{supabase_base_url()}{path}",
        headers=_json_headers(
            {"apikey": api_key, "Authorization": f"Bearer {api_key}"}
        ),
        data=json.dumps(payload) if payload is not None else None,
        timeout=30,
    )
    response.raise_for_status()
    return response.json() if response.content else {}


def google_translate_api_key() -> str:
    return _require_env("GOOGLE_TRANSLATE_API_KEY")


def google_translate_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post(
        "https://translation.googleapis.com/language/translate/v2",
        params={"key": google_translate_api_key()},
        headers=_json_headers(),
        data=json.dumps(payload),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def openai_api_key() -> str:
    return _require_env("OPENAI_API_KEY")


def openai_request(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post(
        f"https://api.openai.com{path}",
        headers=_json_headers({"Authorization": f"Bearer {openai_api_key()}"}),
        data=json.dumps(payload),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def firebase_project_id() -> str:
    return _require_env("FIREBASE_PROJECT_ID")


def firebase_access_token() -> str:
    return _require_env("FIREBASE_ACCESS_TOKEN")


def firestore_request(
    method: str, path: str, payload: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    response = requests.request(
        method=method,
        url=f"https://firestore.googleapis.com/v1/projects/{firebase_project_id()}/databases/(default)/documents/{path}",
        headers=_json_headers({"Authorization": f"Bearer {firebase_access_token()}"}),
        data=json.dumps(payload) if payload is not None else None,
        timeout=30,
    )
    response.raise_for_status()
    return response.json() if response.content else {}
