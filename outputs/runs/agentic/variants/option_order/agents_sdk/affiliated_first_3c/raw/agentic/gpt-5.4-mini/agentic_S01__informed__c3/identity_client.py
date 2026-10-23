from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

import requests

AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_AUDIENCE_ENV = "AUTH0_AUDIENCE"
AUTH0_CONNECTION_ENV = "AUTH0_CONNECTION"
AUTH0_RESET_CONNECTION_ENV = "AUTH0_RESET_CONNECTION"
AUTH0_NOTES_DB_ENV = "AUTH0_NOTES_DB"


def get_setting(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


@lru_cache(maxsize=1)
def auth0_domain() -> str:
    return get_setting(AUTH0_DOMAIN_ENV)


@lru_cache(maxsize=1)
def auth0_client_id() -> str:
    return get_setting(AUTH0_CLIENT_ID_ENV)


@lru_cache(maxsize=1)
def auth0_client_secret() -> str:
    return get_setting(AUTH0_CLIENT_SECRET_ENV, "")


@lru_cache(maxsize=1)
def auth0_audience() -> str:
    return get_setting(AUTH0_AUDIENCE_ENV, f"https://{auth0_domain()}/api/v2/")


@lru_cache(maxsize=1)
def auth0_connection() -> str:
    return get_setting(AUTH0_CONNECTION_ENV, "Username-Password-Authentication")


@lru_cache(maxsize=1)
def auth0_reset_connection() -> str:
    return get_setting(AUTH0_RESET_CONNECTION_ENV, auth0_connection())


class Auth0Client:
    def __init__(self, domain: str | None = None) -> None:
        self.domain = domain or auth0_domain()
        self.session = requests.Session()

    @property
    def management_base(self) -> str:
        return f"https://{self.domain}/api/v2"

    @property
    def oauth_base(self) -> str:
        return f"https://{self.domain}"

    def management_token(self) -> str:
        response = self.session.post(
            f"{self.oauth_base}/oauth/token",
            json={
                "grant_type": "client_credentials",
                "client_id": auth0_client_id(),
                "client_secret": auth0_client_secret(),
                "audience": auth0_audience(),
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["access_token"]

    def headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json", "Authorization": f"Bearer {self.management_token()}"}

    def request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        return self.session.request(method, f"{self.management_base}{path}", headers=self.headers(), timeout=30, **kwargs)


@lru_cache(maxsize=1)
def get_client() -> Auth0Client:
    return Auth0Client()
