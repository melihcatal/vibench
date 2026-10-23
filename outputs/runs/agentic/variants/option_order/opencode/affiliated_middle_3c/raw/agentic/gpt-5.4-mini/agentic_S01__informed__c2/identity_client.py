import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Auth0Config:
    domain: str
    client_id: str
    client_secret: str
    audience: str
    connection: str
    scope: str = "openid profile email offline_access"


def get_auth0_config():
    return Auth0Config(
        domain=os.environ["AUTH0_DOMAIN"],
        client_id=os.environ["AUTH0_CLIENT_ID"],
        client_secret=os.environ["AUTH0_CLIENT_SECRET"],
        audience=os.environ.get("AUTH0_AUDIENCE", f"https://{os.environ['AUTH0_DOMAIN']}/api/v2/"),
        connection=os.environ.get("AUTH0_CONNECTION", "Username-Password-Authentication"),
    )


def build_base_url(cfg):
    return f"https://{cfg.domain}"


def build_headers(cfg):
    return {"content-type": "application/json"}
