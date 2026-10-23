import os
from dataclasses import dataclass
from typing import Optional

from authlib.integrations.requests_client import OAuth2Session


@dataclass
class IdentityProviderConfig:
    issuer: str
    client_id: str
    client_secret: Optional[str]
    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str
    redirect_uri: str
    scope: str = "openid profile email"


def load_identity_provider_config(prefix: str = "OIDC") -> IdentityProviderConfig:
    return IdentityProviderConfig(
        issuer=os.environ[f"{prefix}_ISSUER"],
        client_id=os.environ[f"{prefix}_CLIENT_ID"],
        client_secret=os.getenv(f"{prefix}_CLIENT_SECRET"),
        authorization_endpoint=os.environ[f"{prefix}_AUTHORIZATION_ENDPOINT"],
        token_endpoint=os.environ[f"{prefix}_TOKEN_ENDPOINT"],
        userinfo_endpoint=os.environ[f"{prefix}_USERINFO_ENDPOINT"],
        redirect_uri=os.environ[f"{prefix}_REDIRECT_URI"],
        scope=os.getenv(f"{prefix}_SCOPE", "openid profile email"),
    )


def create_oauth_session(
    config: IdentityProviderConfig,
    state: Optional[str] = None,
    code_verifier: Optional[str] = None,
) -> OAuth2Session:
    return OAuth2Session(
        client_id=config.client_id,
        client_secret=config.client_secret,
        scope=config.scope,
        redirect_uri=config.redirect_uri,
        state=state,
        code_verifier=code_verifier,
    )


def build_authorization_url(
    config: IdentityProviderConfig,
    state: str,
    code_challenge: Optional[str] = None,
    code_challenge_method: str = "S256",
):
    session = create_oauth_session(config, state=state)
    kwargs = {"access_type": "offline"}
    if code_challenge:
        kwargs["code_challenge"] = code_challenge
        kwargs["code_challenge_method"] = code_challenge_method
    return session.create_authorization_url(config.authorization_endpoint, **kwargs)
