import os
from dataclasses import dataclass
from typing import Optional


AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_REDIRECT_URI_ENV = "AUTH0_REDIRECT_URI"
AUTH0_ISSUER_ENV = "AUTH0_ISSUER"
AUTH0_AUTHORIZE_PATH = "/authorize"
AUTH0_TOKEN_PATH = "/oauth/token"
AUTH0_USERINFO_PATH = "/userinfo"
AUTH0_SCOPE = "openid profile email"


@dataclass(frozen=True)
class IdentityClientConfig:
    domain: str
    client_id: str
    redirect_uri: str
    client_secret: Optional[str] = None
    issuer: Optional[str] = None
    scope: str = AUTH0_SCOPE

    @property
    def base_url(self) -> str:
        return f"https://{self.domain.rstrip('/')}"

    @property
    def authorize_url(self) -> str:
        return f"{self.base_url}{AUTH0_AUTHORIZE_PATH}"

    @property
    def token_url(self) -> str:
        return f"{self.base_url}{AUTH0_TOKEN_PATH}"

    @property
    def userinfo_url(self) -> str:
        return f"{self.base_url}{AUTH0_USERINFO_PATH}"

    @property
    def effective_issuer(self) -> str:
        return self.issuer or self.base_url


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"{name} is required")
    return value


def load_identity_client_config() -> IdentityClientConfig:
    return IdentityClientConfig(
        domain=_require_env(AUTH0_DOMAIN_ENV),
        client_id=_require_env(AUTH0_CLIENT_ID_ENV),
        redirect_uri=_require_env(AUTH0_REDIRECT_URI_ENV),
        client_secret=os.getenv(AUTH0_CLIENT_SECRET_ENV),
        issuer=os.getenv(AUTH0_ISSUER_ENV),
    )


def build_authorization_params(
    config: IdentityClientConfig,
    state: str,
    nonce: str,
    code_challenge: str,
    code_challenge_method: str = "S256",
    audience: Optional[str] = None,
    organization: Optional[str] = None,
    connection: Optional[str] = None,
) -> dict:
    params = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "response_type": "code",
        "scope": config.scope,
        "state": state,
        "nonce": nonce,
        "code_challenge": code_challenge,
        "code_challenge_method": code_challenge_method,
    }
    if audience:
        params["audience"] = audience
    if organization:
        params["organization"] = organization
    if connection:
        params["connection"] = connection
    return params


def build_token_exchange_payload(
    config: IdentityClientConfig,
    code: str,
    code_verifier: str,
) -> dict:
    payload = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "code": code,
        "redirect_uri": config.redirect_uri,
        "code_verifier": code_verifier,
    }
    if config.client_secret:
        payload["client_secret"] = config.client_secret
    return payload


def build_userinfo_headers(access_token: str) -> dict:
    return {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}


def resolve_identity_client_config(
    client_id: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    domain: Optional[str] = None,
    client_secret: Optional[str] = None,
    issuer: Optional[str] = None,
) -> IdentityClientConfig:
    return IdentityClientConfig(
        domain=domain or _require_env(AUTH0_DOMAIN_ENV),
        client_id=client_id or _require_env(AUTH0_CLIENT_ID_ENV),
        redirect_uri=redirect_uri or _require_env(AUTH0_REDIRECT_URI_ENV),
        client_secret=client_secret if client_secret is not None else os.getenv(AUTH0_CLIENT_SECRET_ENV),
        issuer=issuer if issuer is not None else os.getenv(AUTH0_ISSUER_ENV),
    )
