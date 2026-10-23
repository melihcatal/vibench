import os
from dataclasses import dataclass
from typing import Any, Mapping, Optional


DEFAULT_PROVIDER = "auth0"
DEFAULT_AUTH0_AUTHORIZE_URL = "https://{domain}/authorize"
DEFAULT_AUTH0_TOKEN_URL = "https://{domain}/oauth/token"
DEFAULT_GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
DEFAULT_GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


@dataclass(frozen=True)
class IdentityClientConfig:
    provider: str
    domain: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    redirect_uri: Optional[str] = None
    audience: Optional[str] = None
    scope: str = "openid profile email"
    token_url: Optional[str] = None
    authorize_url: Optional[str] = None
    userinfo_url: Optional[str] = None


class IdentityClientError(Exception):
    pass


def load_identity_config(env: Mapping[str, str] | None = None) -> IdentityClientConfig:
    source = env or os.environ
    provider = (source.get("IDENTITY_PROVIDER") or DEFAULT_PROVIDER).lower()
    domain = source.get("AUTH0_DOMAIN") or source.get("GOOGLE_OAUTH_DOMAIN")
    client_id = source.get("AUTH0_CLIENT_ID") or source.get("GOOGLE_OAUTH_CLIENT_ID")
    client_secret = source.get("AUTH0_CLIENT_SECRET") or source.get("GOOGLE_OAUTH_CLIENT_SECRET")
    redirect_uri = source.get("AUTH0_REDIRECT_URI") or source.get("GOOGLE_OAUTH_REDIRECT_URI")
    audience = source.get("AUTH0_AUDIENCE") or source.get("GOOGLE_OAUTH_AUDIENCE")
    scope = source.get("AUTH0_SCOPE") or source.get("GOOGLE_OAUTH_SCOPE") or "openid profile email"

    if provider == "google":
        token_url = source.get("GOOGLE_OAUTH_TOKEN_URL") or DEFAULT_GOOGLE_TOKEN_URL
        userinfo_url = source.get("GOOGLE_OAUTH_USERINFO_URL") or DEFAULT_GOOGLE_USERINFO_URL
        authorize_url = source.get("GOOGLE_OAUTH_AUTHORIZE_URL")
    else:
        token_url = source.get("AUTH0_TOKEN_URL") or (DEFAULT_AUTH0_TOKEN_URL.format(domain=domain or "" ) if domain else None)
        userinfo_url = source.get("AUTH0_USERINFO_URL")
        authorize_url = source.get("AUTH0_AUTHORIZE_URL") or (DEFAULT_AUTH0_AUTHORIZE_URL.format(domain=domain or "" ) if domain else None)

    return IdentityClientConfig(
        provider=provider,
        domain=domain,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        audience=audience,
        scope=scope,
        token_url=token_url,
        authorize_url=authorize_url,
        userinfo_url=userinfo_url,
    )


def get_identity_client_config(env: Mapping[str, str] | None = None) -> dict[str, Any]:
    config = load_identity_config(env)
    return {
        "provider": config.provider,
        "domain": config.domain,
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "redirect_uri": config.redirect_uri,
        "audience": config.audience,
        "scope": config.scope,
        "token_url": config.token_url,
        "authorize_url": config.authorize_url,
        "userinfo_url": config.userinfo_url,
    }


def require_identity_value(value: Optional[str], name: str) -> str:
    if not value:
        raise IdentityClientError(f"{name} is required")
    return value


def build_provider_headers(access_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {access_token}"}


def normalize_identity_payload(payload: Mapping[str, Any], provider: str | None = None) -> dict[str, Any]:
    provider_name = (provider or payload.get("provider") or DEFAULT_PROVIDER).lower()
    subject = payload.get("sub") or payload.get("subject") or payload.get("id")
    email = payload.get("email")
    given_name = payload.get("given_name") or payload.get("first_name")
    family_name = payload.get("family_name") or payload.get("last_name")
    name = payload.get("name")
    if not name:
        parts = [part for part in (given_name, family_name) if part]
        name = " ".join(parts) if parts else email or subject
    return {
        "provider": provider_name,
        "subject": subject,
        "email": email,
        "email_verified": payload.get("email_verified"),
        "given_name": given_name,
        "family_name": family_name,
        "name": name,
        "picture": payload.get("picture"),
        "locale": payload.get("locale"),
        "raw": dict(payload),
    }
