from dataclasses import dataclass


@dataclass
class OAuthConfig:
    domain_prefix: str
    region: str
    client_id: str
    client_secret: str | None = None
    identity_provider: str | None = None


def get_oauth_config(config=None):
    config = config or {}
    return OAuthConfig(
        domain_prefix=config["domain_prefix"],
        region=config["region"],
        client_id=config["client_id"],
        client_secret=config.get("client_secret"),
        identity_provider=config.get("identity_provider"),
    )


def get_cognito_base_url(cfg):
    return f"https://{cfg.domain_prefix}.auth.{cfg.region}.amazoncognito.com"
