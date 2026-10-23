import os
from dataclasses import dataclass

import requests


@dataclass
class IdentityClientConfig:
    auth0_domain: str
    auth0_client_id: str
    auth0_client_secret: str
    auth0_audience: str


def load_identity_config() -> IdentityClientConfig:
    return IdentityClientConfig(
        auth0_domain=os.environ["AUTH0_DOMAIN"],
        auth0_client_id=os.environ["AUTH0_CLIENT_ID"],
        auth0_client_secret=os.environ.get("AUTH0_CLIENT_SECRET", ""),
        auth0_audience=os.environ.get(
            "AUTH0_AUDIENCE", f"https://{os.environ['AUTH0_DOMAIN']}/api/v2/"
        ),
    )


def auth0_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    return session
