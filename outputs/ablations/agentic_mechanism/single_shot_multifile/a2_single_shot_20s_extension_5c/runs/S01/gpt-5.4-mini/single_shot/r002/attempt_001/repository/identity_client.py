import os
from dataclasses import dataclass
from typing import Dict, Optional

AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_AUDIENCE_ENV = "AUTH0_AUDIENCE"
AUTH0_DATABASE_CONNECTION_ENV = "AUTH0_DATABASE_CONNECTION"
AUTH0_ORGANIZATION_ID_ENV = "AUTH0_ORGANIZATION_ID"
AUTH0_MANAGEMENT_API_TOKEN_ENV = "AUTH0_MANAGEMENT_API_TOKEN"


@dataclass(frozen=True)
class IdentityConfig:
    auth0_domain: str
    auth0_client_id: str
    auth0_client_secret: str
    auth0_audience: str
    auth0_database_connection: str
    auth0_organization_id: Optional[str]
    auth0_management_api_token: Optional[str]
    timeout_seconds: float = 20.0



def get_identity_config() -> IdentityConfig:
    return IdentityConfig(
        auth0_domain=os.environ[AUTH0_DOMAIN_ENV],
        auth0_client_id=os.environ[AUTH0_CLIENT_ID_ENV],
        auth0_client_secret=os.environ.get(AUTH0_CLIENT_SECRET_ENV, ""),
        auth0_audience=os.environ.get(AUTH0_AUDIENCE_ENV, ""),
        auth0_database_connection=os.environ.get(AUTH0_DATABASE_CONNECTION_ENV, "Username-Password-Authentication"),
        auth0_organization_id=os.environ.get(AUTH0_ORGANIZATION_ID_ENV),
        auth0_management_api_token=os.environ.get(AUTH0_MANAGEMENT_API_TOKEN_ENV),
    )



def build_url(cfg: IdentityConfig, path: str) -> str:
    return f"https://{cfg.auth0_domain}{path}"



def build_headers(cfg: IdentityConfig, content_type: str = "application/json") -> Dict[str, str]:
    headers = {"Content-Type": content_type}
    if cfg.auth0_management_api_token:
        headers["Authorization"] = f"Bearer {cfg.auth0_management_api_token}"
    return headers



def normalize_locale(locale: Optional[str]) -> Optional[str]:
    if not locale:
        return None
    value = locale.strip().replace("_", "-")
    return value.lower() if len(value) == 2 else value
