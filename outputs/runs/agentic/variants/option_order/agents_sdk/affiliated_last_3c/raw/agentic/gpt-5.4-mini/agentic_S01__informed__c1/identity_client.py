from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import boto3
from botocore.client import BaseClient

from identity_models import (
    IdentityTokens,
    IdentityUser,
    ResetStartResult,
    normalize_email,
)


@dataclass(frozen=True)
class IdentityConfig:
    user_pool_id: str
    client_id: str
    region_name: str | None = None

    @classmethod
    def from_env(cls) -> "IdentityConfig":
        return cls(
            user_pool_id=os.environ["COGNITO_USER_POOL_ID"],
            client_id=os.environ["COGNITO_APP_CLIENT_ID"],
            region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        )


class CognitoIdentityClient:
    def __init__(self, config: IdentityConfig | None = None, client: BaseClient | None = None):
        self.config = config or IdentityConfig.from_env()
        self.client = client or boto3.client("cognito-idp", region_name=self.config.region_name)

    def register_user(self, email: str, password: str, given_name: str | None = None, family_name: str | None = None, locale: str | None = None) -> IdentityUser:
        attrs = [{"Name": "email", "Value": normalize_email(email)}]
        if given_name:
            attrs.append({"Name": "given_name", "Value": given_name})
        if family_name:
            attrs.append({"Name": "family_name", "Value": family_name})
        if locale:
            attrs.append({"Name": "locale", "Value": locale})
        response = self.client.sign_up(
            ClientId=self.config.client_id,
            Username=normalize_email(email),
            Password=password,
            UserAttributes=attrs,
        )
        return IdentityUser(user_id=response.get("UserSub", ""), email=normalize_email(email), enabled=not response.get("UserConfirmed", False), locale=locale)

    def login(self, email: str, password: str) -> IdentityTokens:
        response = self.client.initiate_auth(
            ClientId=self.config.client_id,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": normalize_email(email), "PASSWORD": password},
        )
        result = response.get("AuthenticationResult", {})
        return IdentityTokens(
            access_token=result.get("AccessToken", ""),
            refresh_token=result.get("RefreshToken"),
            id_token=result.get("IdToken"),
            expires_in=result.get("ExpiresIn"),
            token_type=result.get("TokenType", "Bearer"),
        )

    def refresh(self, refresh_token: str) -> IdentityTokens:
        response = self.client.initiate_auth(
            ClientId=self.config.client_id,
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={"REFRESH_TOKEN": refresh_token},
        )
        result = response.get("AuthenticationResult", {})
        return IdentityTokens(
            access_token=result.get("AccessToken", ""),
            refresh_token=refresh_token,
            id_token=result.get("IdToken"),
            expires_in=result.get("ExpiresIn"),
            token_type=result.get("TokenType", "Bearer"),
        )

    def start_password_reset(self, email: str) -> ResetStartResult:
        response = self.client.forgot_password(ClientId=self.config.client_id, Username=normalize_email(email))
        code_delivery = response.get("CodeDeliveryDetails", {})
        return ResetStartResult(
            email=normalize_email(email),
            delivery_medium=code_delivery.get("DeliveryMedium"),
            request_id=response.get("ResponseMetadata", {}).get("RequestId"),
        )
