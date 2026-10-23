from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional


DEFAULT_PROVIDER = "auth0"


@dataclass(frozen=True)
class IdentityConfig:
    provider: str
    domain: str
    audience: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    connection: Optional[str] = None
    scope: str = "openid profile email offline_access"

    @property
    def token_endpoint(self) -> str:
        return f"https://{self.domain}/oauth/token"

    @property
    def userinfo_endpoint(self) -> str:
        return f"https://{self.domain}/userinfo"


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in (None, "") else default


def load_identity_config() -> IdentityConfig:
    provider = _env("IDENTITY_PROVIDER", DEFAULT_PROVIDER) or DEFAULT_PROVIDER
    domain = _env("AUTH0_DOMAIN") or _env("IDENTITY_DOMAIN")
    if not domain:
        raise ValueError("AUTH0_DOMAIN or IDENTITY_DOMAIN is required")
    return IdentityConfig(
        provider=provider,
        domain=domain,
        audience=_env("AUTH0_AUDIENCE") or _env("IDENTITY_AUDIENCE"),
        client_id=_env("AUTH0_CLIENT_ID") or _env("IDENTITY_CLIENT_ID"),
        client_secret=_env("AUTH0_CLIENT_SECRET") or _env("IDENTITY_CLIENT_SECRET"),
        connection=_env("AUTH0_CONNECTION") or _env("IDENTITY_CONNECTION"),
        scope=_env("AUTH0_SCOPE", "openid profile email offline_access") or "openid profile email offline_access",
    )


@lru_cache(maxsize=1)
def get_identity_config() -> IdentityConfig:
    return load_identity_config()


def clear_identity_config_cache() -> None:
    get_identity_config.cache_clear()


def require_client_credentials(config: Optional[IdentityConfig] = None) -> tuple[str, str]:
    cfg = config or get_identity_config()
    if not cfg.client_id or not cfg.client_secret:
        raise ValueError("Identity client credentials are required")
    return cfg.client_id, cfg.client_secret


def require_domain(config: Optional[IdentityConfig] = None) -> str:
    cfg = config or get_identity_config()
    if not cfg.domain:
        raise ValueError("Identity domain is required")
    return cfg.domain
