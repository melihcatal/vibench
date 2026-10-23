import os
from typing import Dict, Optional


def auth0_domain() -> str:
    return os.environ["AUTH0_DOMAIN"]


def auth0_client_id() -> str:
    return os.environ["AUTH0_CLIENT_ID"]


def auth0_client_secret() -> Optional[str]:
    return os.getenv("AUTH0_CLIENT_SECRET")


def auth0_audience() -> Optional[str]:
    return os.getenv("AUTH0_AUDIENCE")


def auth0_management_base_url() -> str:
    return f"https://{auth0_domain()}/api/v2"


def auth0_auth_base_url() -> str:
    return f"https://{auth0_domain()}"


def auth0_headers(token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
