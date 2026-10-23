import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class IdentityConfig:
    auth0_domain: str
    auth0_client_id: str
    auth0_client_secret: Optional[str]
    auth0_audience: Optional[str]
    auth0_connection: Optional[str]
    auth0_reset_connection: Optional[str]


def load_identity_config() -> IdentityConfig:
    return IdentityConfig(
        auth0_domain=os.environ["AUTH0_DOMAIN"],
        auth0_client_id=os.environ["AUTH0_CLIENT_ID"],
        auth0_client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
        auth0_audience=os.environ.get("AUTH0_AUDIENCE"),
        auth0_connection=os.environ.get(
            "AUTH0_CONNECTION", "Username-Password-Authentication"
        ),
        auth0_reset_connection=os.environ.get(
            "AUTH0_RESET_CONNECTION",
            os.environ.get("AUTH0_CONNECTION", "Username-Password-Authentication"),
        ),
    )


def auth0_url(domain: str, path: str) -> str:
    return f"https://{domain}{path}"


def normalize_email(email: str) -> str:
    return email.strip().lower()


def bearer_headers(access_token: str) -> dict:
    return {"Authorization": f"Bearer {access_token}"}
