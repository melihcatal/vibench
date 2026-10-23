import os
from dataclasses import dataclass


@dataclass
class IdentityConfig:
    region: str
    domain_prefix: str
    client_id: str
    client_secret: str | None = None
    issuer_url: str | None = None
    redirect_uri: str | None = None


def load_identity_config(config=None):
    config = config or {}
    return IdentityConfig(
        region=config.get("region") or os.environ.get("COGNITO_REGION", "us-east-1"),
        domain_prefix=config.get("domain_prefix") or os.environ.get("COGNITO_DOMAIN_PREFIX", "example"),
        client_id=config.get("client_id") or os.environ.get("COGNITO_CLIENT_ID", "client"),
        client_secret=config.get("client_secret") or os.environ.get("COGNITO_CLIENT_SECRET"),
        issuer_url=config.get("issuer_url") or os.environ.get("COGNITO_ISSUER_URL"),
        redirect_uri=config.get("redirect_uri") or os.environ.get("COGNITO_REDIRECT_URI"),
    )


def cognito_domain(config):
    return f"https://{config.domain_prefix}.auth.{config.region}.amazoncognito.com"


def basic_auth_headers(client_id, client_secret):
    if not client_secret:
        return {}
    import base64

    token = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    return {"Authorization": f"Basic {token}"}
