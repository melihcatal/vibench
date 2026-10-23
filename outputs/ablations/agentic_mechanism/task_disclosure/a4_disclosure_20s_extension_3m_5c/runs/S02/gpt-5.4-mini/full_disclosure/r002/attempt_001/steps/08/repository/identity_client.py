import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


DEFAULT_PROVIDER = "okta"
DEFAULT_ISSUER = "https://dev-00000000.okta.com/oauth2/default"


@dataclass(frozen=True)
class IdentityClientConfig:
    provider: str
    issuer: str
    client_id: Optional[str]
    client_secret: Optional[str]
    redirect_uri: Optional[str]
    scope: str
    authorize_path: str
    token_path: str
    userinfo_path: str

    @property
    def authorization_endpoint(self) -> str:
        return f"{self.issuer.rstrip('/')}{self.authorize_path}"

    @property
    def token_endpoint(self) -> str:
        return f"{self.issuer.rstrip('/')}{self.token_path}"

    @property
    def userinfo_endpoint(self) -> str:
        return f"{self.issuer.rstrip('/')}{self.userinfo_path}"


def load_identity_client_config(env: Optional[Dict[str, str]] = None) -> IdentityClientConfig:
    env = env or os.environ
    provider = env.get("IDENTITY_PROVIDER", DEFAULT_PROVIDER).strip() or DEFAULT_PROVIDER
    issuer = env.get("OKTA_OAUTH_BASE_URL", env.get("IDENTITY_ISSUER", DEFAULT_ISSUER)).strip() or DEFAULT_ISSUER
    return IdentityClientConfig(
        provider=provider,
        issuer=issuer,
        client_id=env.get("OKTA_CLIENT_ID") or env.get("IDENTITY_CLIENT_ID"),
        client_secret=env.get("OKTA_CLIENT_SECRET") or env.get("IDENTITY_CLIENT_SECRET"),
        redirect_uri=env.get("OKTA_REDIRECT_URI") or env.get("IDENTITY_REDIRECT_URI"),
        scope=env.get("OKTA_SCOPE") or env.get("IDENTITY_SCOPE", "openid profile email"),
        authorize_path=env.get("IDENTITY_AUTHORIZE_PATH", "/v1/authorize"),
        token_path=env.get("IDENTITY_TOKEN_PATH", "/v1/token"),
        userinfo_path=env.get("IDENTITY_USERINFO_PATH", "/v1/userinfo"),
    )


def require_client_credentials(config: IdentityClientConfig) -> tuple[str, str]:
    if not config.client_id:
        raise ValueError("missing_client_id")
    if not config.client_secret:
        raise ValueError("missing_client_secret")
    return config.client_id, config.client_secret


def build_authorization_request_params(
    config: IdentityClientConfig,
    state: str,
    code_challenge: str,
    response_type: str = "code",
) -> Dict[str, str]:
    if not config.client_id:
        raise ValueError("missing_client_id")
    if not config.redirect_uri:
        raise ValueError("missing_redirect_uri")
    return {
        "response_type": response_type,
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "scope": config.scope,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }


def normalize_identity_error(payload: Any) -> str:
    if isinstance(payload, dict):
        error = payload.get("error")
        description = payload.get("error_description") or payload.get("message")
        if error and description:
            return f"{error}: {description}"
        if error:
            return str(error)
        if description:
            return str(description)
    return "identity_request_failed"


def identity_headers(access_token: Optional[str] = None, accept_json: bool = True) -> Dict[str, str]:
    headers = {}
    if accept_json:
        headers["Accept"] = "application/json"
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    return headers
