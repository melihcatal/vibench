import os
from dataclasses import dataclass
from typing import Optional


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name, default)
    return value if value not in ("", None) else default


@dataclass(frozen=True)
class IdentityConfig:
    auth0_domain: str
    auth0_client_id: str
    auth0_client_secret: str
    auth0_audience: str
    auth0_connection: str
    auth0_management_audience: str
    locale: str


def load_identity_config() -> IdentityConfig:
    return IdentityConfig(
        auth0_domain=_env("AUTH0_DOMAIN", "example.auth0.com"),
        auth0_client_id=_env("AUTH0_CLIENT_ID", "client_id"),
        auth0_client_secret=_env("AUTH0_CLIENT_SECRET", "client_secret"),
        auth0_audience=_env("AUTH0_AUDIENCE", f"https://{_env('AUTH0_DOMAIN', 'example.auth0.com')}/api/v2/"),
        auth0_connection=_env("AUTH0_CONNECTION", "Username-Password-Authentication"),
        auth0_management_audience=_env("AUTH0_MANAGEMENT_AUDIENCE", f"https://{_env('AUTH0_DOMAIN', 'example.auth0.com')}/api/v2/"),
        locale=_env("APP_LOCALE", "en"),
    )


def auth0_issuer_domain(config: Optional[IdentityConfig] = None) -> str:
    return (config or load_identity_config()).auth0_domain
