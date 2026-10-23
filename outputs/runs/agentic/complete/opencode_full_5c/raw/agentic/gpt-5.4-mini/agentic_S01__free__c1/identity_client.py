import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

import httpx

from identity_models import normalize_email, normalize_locale, normalize_password


@dataclass(frozen=True)
class IdentityConfig:
    base_url: str
    api_key: str
    timeout: float


@lru_cache(maxsize=1)
def get_identity_config() -> IdentityConfig:
    return IdentityConfig(
        base_url=os.environ.get(
            "IDENTITY_API_BASE_URL", "https://identitytoolkit.googleapis.com"
        ),
        api_key=os.environ.get(
            "FIREBASE_WEB_API_KEY", os.environ.get("IDENTITY_API_KEY", "")
        ),
        timeout=float(os.environ.get("IDENTITY_HTTP_TIMEOUT", "20")),
    )


def build_client() -> httpx.Client:
    cfg = get_identity_config()
    return httpx.Client(base_url=cfg.base_url, timeout=cfg.timeout)


def auth_headers() -> Dict[str, str]:
    return {"Content-Type": "application/json"}


def require_api_key() -> str:
    api_key = get_identity_config().api_key
    if not api_key:
        raise RuntimeError("Missing FIREBASE_WEB_API_KEY or IDENTITY_API_KEY")
    return api_key


def build_query() -> Dict[str, str]:
    return {"key": require_api_key()}


def normalize_identity_input(
    email: str, password: Optional[str] = None, locale: Optional[str] = None
) -> Dict[str, Any]:
    data: Dict[str, Any] = {"email": normalize_email(email)}
    if password is not None:
        data["password"] = normalize_password(password)
    if locale is not None:
        data["locale"] = normalize_locale(locale)
    return data
