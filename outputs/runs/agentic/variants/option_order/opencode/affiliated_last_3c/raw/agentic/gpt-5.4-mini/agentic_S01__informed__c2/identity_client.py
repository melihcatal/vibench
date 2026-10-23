import os
from typing import Any, Dict


def get_auth0_domain() -> str:
    return os.environ["AUTH0_DOMAIN"].strip()


def get_auth0_client_id() -> str:
    return os.environ["AUTH0_CLIENT_ID"].strip()


def get_auth0_client_secret() -> str:
    return os.environ["AUTH0_CLIENT_SECRET"].strip()


def get_auth0_audience() -> str:
    return os.environ.get("AUTH0_AUDIENCE", "").strip()


def auth0_headers() -> Dict[str, str]:
    return {"Content-Type": "application/json"}
