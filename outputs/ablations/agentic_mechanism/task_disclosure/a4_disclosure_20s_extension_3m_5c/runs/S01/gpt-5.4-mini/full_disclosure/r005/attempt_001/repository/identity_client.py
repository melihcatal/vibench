import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional


@dataclass(frozen=True)
class IdentityConfig:
    base_url: str
    api_key: Optional[str]
    tenant_id: Optional[str]
    timeout_seconds: float


def _strip_trailing_slash(value: str) -> str:
    return value[:-1] if value.endswith("/") else value


def get_identity_config() -> IdentityConfig:
    base_url = os.getenv("IDENTITY_API_BASE_URL", "https://api.auth0.com")
    api_key = os.getenv("IDENTITY_API_KEY") or os.getenv("AUTH0_CLIENT_SECRET")
    tenant_id = os.getenv("IDENTITY_TENANT_ID") or os.getenv("AUTH0_TENANT_ID")
    timeout_seconds = float(os.getenv("IDENTITY_API_TIMEOUT_SECONDS", "30"))
    return IdentityConfig(
        base_url=_strip_trailing_slash(base_url),
        api_key=api_key,
        tenant_id=tenant_id,
        timeout_seconds=timeout_seconds,
    )


@lru_cache(maxsize=1)
def get_identity_base_url() -> str:
    return get_identity_config().base_url


def get_identity_api_key() -> Optional[str]:
    return get_identity_config().api_key


def get_identity_tenant_id() -> Optional[str]:
    return get_identity_config().tenant_id


def get_identity_timeout_seconds() -> float:
    return get_identity_config().timeout_seconds


def build_identity_headers() -> dict:
    headers = {"Content-Type": "application/json"}
    api_key = get_identity_api_key()
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    tenant_id = get_identity_tenant_id()
    if tenant_id:
        headers["X-Tenant-Id"] = tenant_id
    return headers


def build_identity_url(path: str) -> str:
    base_url = get_identity_base_url()
    path = path if path.startswith("/") else f"/{path}"
    return f"{base_url}{path}"
