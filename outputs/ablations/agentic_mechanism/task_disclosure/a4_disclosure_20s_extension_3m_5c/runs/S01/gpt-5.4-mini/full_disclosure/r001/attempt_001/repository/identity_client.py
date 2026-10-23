import os
from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional


DEFAULT_IDENTITY_API_BASE_URL = "https://identitytoolkit.googleapis.com/v1"
DEFAULT_IDENTITY_REST_API_BASE_URL = "https://identitytoolkit.googleapis.com/v1"
DEFAULT_IDENTITY_PROVIDER = "firebase_auth"


def _env(key: str, default: str = "") -> str:
    value = os.getenv(key, default)
    return value.strip() if isinstance(value, str) else default


def _first_non_empty(*values: Optional[str]) -> str:
    for value in values:
        if value and str(value).strip():
            return str(value).strip()
    return ""


@dataclass(frozen=True)
class IdentityClientConfig:
    api_key: str = ""
    project_id: str = ""
    tenant_id: str = ""
    auth_domain: str = ""
    api_base_url: str = DEFAULT_IDENTITY_API_BASE_URL
    rest_api_base_url: str = DEFAULT_IDENTITY_REST_API_BASE_URL
    provider: str = DEFAULT_IDENTITY_PROVIDER
    extra_headers: Mapping[str, str] = field(default_factory=dict)

    @classmethod
    def from_env(cls) -> "IdentityClientConfig":
        return cls(
            api_key=_first_non_empty(_env("FIREBASE_WEB_API_KEY"), _env("GOOGLE_API_KEY"), _env("IDENTITY_API_KEY")),
            project_id=_first_non_empty(_env("FIREBASE_PROJECT_ID"), _env("GOOGLE_CLOUD_PROJECT"), _env("IDENTITY_PROJECT_ID")),
            tenant_id=_first_non_empty(_env("FIREBASE_TENANT_ID"), _env("IDENTITY_TENANT_ID")),
            auth_domain=_first_non_empty(_env("FIREBASE_AUTH_DOMAIN"), _env("IDENTITY_AUTH_DOMAIN")),
            api_base_url=_first_non_empty(_env("FIREBASE_IDENTITY_API_BASE_URL"), _env("IDENTITY_API_BASE_URL"), DEFAULT_IDENTITY_API_BASE_URL),
            rest_api_base_url=_first_non_empty(_env("FIREBASE_IDENTITY_REST_API_BASE_URL"), _env("IDENTITY_REST_API_BASE_URL"), DEFAULT_IDENTITY_REST_API_BASE_URL),
            provider=_first_non_empty(_env("IDENTITY_PROVIDER"), DEFAULT_IDENTITY_PROVIDER),
            extra_headers=_parse_headers(_env("IDENTITY_EXTRA_HEADERS")),
        )

    def is_configured(self) -> bool:
        return bool(self.api_key and self.project_id)

    def with_overrides(self, **kwargs: Any) -> "IdentityClientConfig":
        data: Dict[str, Any] = {
            "api_key": self.api_key,
            "project_id": self.project_id,
            "tenant_id": self.tenant_id,
            "auth_domain": self.auth_domain,
            "api_base_url": self.api_base_url,
            "rest_api_base_url": self.rest_api_base_url,
            "provider": self.provider,
            "extra_headers": dict(self.extra_headers),
        }
        data.update({k: v for k, v in kwargs.items() if v is not None})
        return IdentityClientConfig(**data)


def _parse_headers(raw: str) -> Mapping[str, str]:
    headers: Dict[str, str] = {}
    if not raw:
        return headers
    for item in raw.split(";"):
        if not item.strip() or "=" not in item:
            continue
        key, value = item.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key:
            headers[key] = value
    return headers


def load_identity_config() -> IdentityClientConfig:
    return IdentityClientConfig.from_env()


def build_identity_endpoint(path: str, config: Optional[IdentityClientConfig] = None) -> str:
    cfg = config or load_identity_config()
    base = cfg.api_base_url.rstrip("/")
    path = path.lstrip("/")
    return f"{base}/{path}"


def build_identity_request_headers(config: Optional[IdentityClientConfig] = None, *, content_type: str = "application/json") -> Dict[str, str]:
    cfg = config or load_identity_config()
    headers: Dict[str, str] = {
        "Content-Type": content_type,
        "X-Client-Provider": cfg.provider,
    }
    if cfg.project_id:
        headers["X-Project-Id"] = cfg.project_id
    if cfg.tenant_id:
        headers["X-Tenant-Id"] = cfg.tenant_id
    if cfg.auth_domain:
        headers["X-Auth-Domain"] = cfg.auth_domain
    headers.update(dict(cfg.extra_headers))
    return headers


def require_identity_api_key(config: Optional[IdentityClientConfig] = None) -> str:
    cfg = config or load_identity_config()
    if not cfg.api_key:
        raise ValueError("Missing Firebase/Identity API key; set FIREBASE_WEB_API_KEY, GOOGLE_API_KEY, or IDENTITY_API_KEY.")
    return cfg.api_key


def require_identity_project_id(config: Optional[IdentityClientConfig] = None) -> str:
    cfg = config or load_identity_config()
    if not cfg.project_id:
        raise ValueError("Missing project id; set FIREBASE_PROJECT_ID, GOOGLE_CLOUD_PROJECT, or IDENTITY_PROJECT_ID.")
    return cfg.project_id


def client_context(config: Optional[IdentityClientConfig] = None) -> Dict[str, Any]:
    cfg = config or load_identity_config()
    return {
        "provider": cfg.provider,
        "configured": cfg.is_configured(),
        "api_key": bool(cfg.api_key),
        "project_id": cfg.project_id,
        "tenant_id": cfg.tenant_id,
        "auth_domain": cfg.auth_domain,
        "api_base_url": cfg.api_base_url,
        "rest_api_base_url": cfg.rest_api_base_url,
        "headers": build_identity_request_headers(cfg),
    }
