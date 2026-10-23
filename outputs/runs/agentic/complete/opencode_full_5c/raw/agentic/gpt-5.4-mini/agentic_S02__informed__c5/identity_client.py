import os
from dataclasses import dataclass


@dataclass
class IdentityConfig:
    issuer: str
    client_id: str
    client_secret: str | None = None
    redirect_uri: str | None = None
    scope: str = "openid profile email"


def load_identity_config(prefix: str = "AUTH0") -> IdentityConfig:
    return IdentityConfig(
        issuer=os.environ.get(f"{prefix}_DOMAIN", ""),
        client_id=os.environ.get(f"{prefix}_CLIENT_ID", ""),
        client_secret=os.environ.get(f"{prefix}_CLIENT_SECRET"),
        redirect_uri=os.environ.get(f"{prefix}_REDIRECT_URI"),
        scope=os.environ.get(f"{prefix}_SCOPE", "openid profile email"),
    )


def authorization_endpoint(config: IdentityConfig) -> str:
    return f"https://{config.issuer}/authorize"


def token_endpoint(config: IdentityConfig) -> str:
    return f"https://{config.issuer}/oauth/token"


def userinfo_endpoint(config: IdentityConfig) -> str:
    return f"https://{config.issuer}/userinfo"
