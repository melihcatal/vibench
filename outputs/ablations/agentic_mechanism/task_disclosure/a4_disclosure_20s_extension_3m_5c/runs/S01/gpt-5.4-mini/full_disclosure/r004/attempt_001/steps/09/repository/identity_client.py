import os
from dataclasses import dataclass
from typing import Optional


AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_CONNECTION_ENV = "AUTH0_CONNECTION"
AUTH0_AUDIENCE_ENV = "AUTH0_AUDIENCE"
AUTH0_SCOPE_ENV = "AUTH0_SCOPE"


@dataclass(frozen=True)
class IdentityConfig:
    domain: str
    client_id: str
    client_secret: str
    connection: str = "Username-Password-Authentication"
    audience: Optional[str] = None
    scope: str = "openid profile email offline_access"


class IdentityClientError(RuntimeError):
    pass


def load_identity_config(
    *,
    domain: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    connection: Optional[str] = None,
    audience: Optional[str] = None,
    scope: Optional[str] = None,
) -> IdentityConfig:
    resolved_domain = domain or os.environ.get(AUTH0_DOMAIN_ENV)
    resolved_client_id = client_id or os.environ.get(AUTH0_CLIENT_ID_ENV)
    resolved_client_secret = client_secret or os.environ.get(AUTH0_CLIENT_SECRET_ENV)
    resolved_connection = connection or os.environ.get(AUTH0_CONNECTION_ENV, "Username-Password-Authentication")
    resolved_audience = audience or os.environ.get(AUTH0_AUDIENCE_ENV)
    resolved_scope = scope or os.environ.get(AUTH0_SCOPE_ENV, "openid profile email offline_access")
    if not resolved_domain or not resolved_client_id or not resolved_client_secret:
        raise IdentityClientError("Missing Auth0 configuration")
    return IdentityConfig(
        domain=resolved_domain,
        client_id=resolved_client_id,
        client_secret=resolved_client_secret,
        connection=resolved_connection,
        audience=resolved_audience,
        scope=resolved_scope,
    )


def auth0_issuer_url(domain: str) -> str:
    return f"https://{domain}/"


def auth0_api_base(domain: str) -> str:
    return f"https://{domain}/api/v2"


def auth0_token_url(domain: str) -> str:
    return f"https://{domain}/oauth/token"


def build_password_realm_payload(config: IdentityConfig, email: str, password: str) -> dict:
    payload = {
        "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "username": email,
        "password": password,
        "realm": config.connection,
        "scope": config.scope,
    }
    if config.audience:
        payload["audience"] = config.audience
    return payload


def build_client_credentials_payload(config: IdentityConfig) -> dict:
    payload = {
        "grant_type": "client_credentials",
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "audience": config.audience or auth0_api_base(config.domain) + "/",
    }
    return payload
