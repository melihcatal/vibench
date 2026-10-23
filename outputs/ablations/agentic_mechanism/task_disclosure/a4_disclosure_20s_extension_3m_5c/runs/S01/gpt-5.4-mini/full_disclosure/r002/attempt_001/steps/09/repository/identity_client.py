from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class IdentityConfig:
    api_base_url: str
    client_id: str
    tenant_id: Optional[str] = None
    audience: Optional[str] = None
    scope: Optional[str] = None


def _env(name: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    value = os.getenv(name, default)
    if required and not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def load_identity_config() -> IdentityConfig:
    api_base_url = _env("IDENTITY_API_BASE_URL", "https://api.clerk.com", required=True)
    client_id = _env("IDENTITY_CLIENT_ID", required=True)
    tenant_id = _env("IDENTITY_TENANT_ID")
    audience = _env("IDENTITY_AUDIENCE")
    scope = _env("IDENTITY_SCOPE")
    return IdentityConfig(
        api_base_url=api_base_url.rstrip("/"),
        client_id=client_id,
        tenant_id=tenant_id,
        audience=audience,
        scope=scope,
    )


def build_identity_headers(config: Optional[IdentityConfig] = None) -> Dict[str, str]:
    cfg = config or load_identity_config()
    headers = {
        "Authorization": f"Bearer {os.getenv('IDENTITY_API_KEY', '')}",
        "X-Client-Id": cfg.client_id,
        "Content-Type": "application/json",
    }
    if cfg.tenant_id:
        headers["X-Tenant-Id"] = cfg.tenant_id
    if cfg.audience:
        headers["X-Audience"] = cfg.audience
    if cfg.scope:
        headers["X-Scope"] = cfg.scope
    return headers


def identity_endpoint(path: str, config: Optional[IdentityConfig] = None) -> str:
    cfg = config or load_identity_config()
    return f"{cfg.api_base_url}/{path.lstrip('/')}"


def normalize_email(email: str) -> str:
    if not isinstance(email, str):
        raise TypeError("email must be a string")
    normalized = email.strip().lower()
    if "@" not in normalized or normalized.startswith("@") or normalized.endswith("@"):
        raise ValueError("invalid email address")
    return normalized


def normalize_locale(locale: Optional[str]) -> str:
    value = (locale or "en").strip()
    return value.replace("_", "-").lower() or "en"


def identity_provider_name() -> str:
    return "clerk"


def client_metadata(config: Optional[IdentityConfig] = None) -> Dict[str, Any]:
    cfg = config or load_identity_config()
    return {
        "provider": identity_provider_name(),
        "client_id": cfg.client_id,
        "tenant_id": cfg.tenant_id,
        "audience": cfg.audience,
        "scope": cfg.scope,
        "base_url": cfg.api_base_url,
    }
