import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Auth0Config:
    domain: str
    client_id: str
    client_secret: str
    management_api_token: str
    connection: str = "Username-Password-Authentication"
    default_audience: str = ""
    default_scope: str = "openid profile email"

    def management_api_url(self) -> str:
        return "https://{}/api/v2/".format(self.domain)

    def oauth_token_url(self) -> str:
        return "https://{}/oauth/token".format(self.domain)

    def dbconnections_url(self) -> str:
        return "https://{}/dbconnections/change_password".format(self.domain)

    def userinfo_url(self) -> str:
        return "https://{}/userinfo".format(self.domain)


def load_auth0_config() -> Auth0Config:
    domain = os.environ.get("AUTH0_DOMAIN", "dev-example.us.auth0.com")
    return Auth0Config(
        domain=domain,
        client_id=os.environ.get("AUTH0_CLIENT_ID", ""),
        client_secret=os.environ.get("AUTH0_CLIENT_SECRET", ""),
        management_api_token=os.environ.get("AUTH0_MANAGEMENT_API_TOKEN", ""),
        connection=os.environ.get(
            "AUTH0_CONNECTION", "Username-Password-Authentication"
        ),
        default_audience=os.environ.get(
            "AUTH0_AUDIENCE", "https://{}/userinfo".format(domain)
        ),
        default_scope=os.environ.get("AUTH0_SCOPE", "openid profile email"),
    )


def build_auth_headers(token: str) -> dict:
    return {
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json",
    }


def build_login_payload(config: Auth0Config, email: str, password: str) -> dict:
    return {
        "grant_type": "password",
        "username": email,
        "password": password,
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "audience": config.default_audience,
        "scope": config.default_scope,
    }


def build_refresh_payload(
    config: Auth0Config,
    refresh_token: str,
    audience: Optional[str] = None,
    scope: Optional[str] = None,
) -> dict:
    payload = {
        "grant_type": "refresh_token",
        "client_id": config.client_id,
        "refresh_token": refresh_token,
    }
    if audience:
        payload["audience"] = audience
    if scope:
        payload["scope"] = scope
    return payload


def build_register_payload(
    config: Auth0Config, email: str, password: str, metadata: Optional[dict] = None
) -> dict:
    return {
        "email": email,
        "password": password,
        "connection": config.connection,
        "user_metadata": metadata or {},
    }


def build_password_reset_payload(config: Auth0Config, email: str) -> dict:
    return {
        "client_id": config.client_id,
        "email": email,
        "connection": config.connection,
    }
