from __future__ import annotations

import os
from typing import Any, Dict, Optional

import boto3
import requests
from openai import OpenAI


class Auth0Client:
    def __init__(self) -> None:
        self.domain = os.environ["AUTH0_DOMAIN"].rstrip("/")
        self.client_id = os.environ["AUTH0_CLIENT_ID"]
        self.client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
        self.timeout = float(os.environ.get("AUTH0_TIMEOUT_SECONDS", "30"))

    @property
    def base_url(self) -> str:
        return f"https://{self.domain}"

    def post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}{path}",
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        if response.content:
            return response.json()
        return {}

    def dbconnections_signup(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        body = {"client_id": self.client_id, **payload}
        return self.post("/dbconnections/signup", body)

    def oauth_token_password(
        self,
        username: str,
        password: str,
        audience: Optional[str],
        scope: str,
        realm: str,
    ) -> Dict[str, Any]:
        body = {
            "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
            "client_id": self.client_id,
            "username": username,
            "password": password,
            "realm": realm,
            "scope": scope,
        }
        if self.client_secret:
            body["client_secret"] = self.client_secret
        if audience:
            body["audience"] = audience
        return self.post("/oauth/token", body)

    def oauth_token_refresh(
        self, refresh_token: str, scope: Optional[str] = None
    ) -> Dict[str, Any]:
        body = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": refresh_token,
        }
        if self.client_secret:
            body["client_secret"] = self.client_secret
        if scope:
            body["scope"] = scope
        return self.post("/oauth/token", body)

    def password_change(self, email: str, connection: str) -> Dict[str, Any]:
        body = {
            "client_id": self.client_id,
            "email": email,
            "connection": connection,
        }
        return self.post("/dbconnections/change_password", body)


def get_auth0_client() -> Auth0Client:
    return Auth0Client()


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def get_dynamodb_table() -> Any:
    region_name = os.environ["AWS_REGION"]
    table_name = os.environ["DYNAMODB_TABLE_NAME"]
    dynamodb = boto3.resource("dynamodb", region_name=region_name)
    return dynamodb.Table(table_name)
