# Local configuration and client helper utilities for Email/Password Account Lifecycle

import os
from typing import Optional, Dict, Any
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0
from auth0.v3.exceptions import Auth0Error
from identity_models import (
    RegisterUserRequest,
    RegisterUserResponse,
    LoginRequest,
    LoginResponse,
    RefreshSessionRequest,
    RefreshSessionResponse,
    PasswordResetRequest,
    PasswordResetResponse,
    normalize_auth0_user_payload,
    normalize_auth0_token_payload
)


class Auth0IdentityClient:
    def __init__(self):
        self.domain = os.getenv("AUTH0_DOMAIN")
        self.client_id = os.getenv("AUTH0_CLIENT_ID")
        self.client_secret = os.getenv("AUTH0_CLIENT_SECRET")
        self.audience = f"https://{self.domain}/api/v2/"
        self.connection = "Username-Password-Authentication"
        self._management_token = None
        self._management_api = None

    def _get_management_token(self) -> str:
        if not self._management_token:
            get_token = GetToken(self.domain)
            token = get_token.client_credentials(
                self.client_id,
                self.client_secret,
                self.audience
            )
            self._management_token = token["access_token"]
        return self._management_token

    def _get_management_api(self) -> Auth0:
        if not self._management_api:
            self._management_api = Auth0(self.domain, self._get_management_token())
        return self._management_api

    def register_user(self, request: RegisterUserRequest) -> RegisterUserResponse:
        api = self._get_management_api()
        user_data = {
            "email": request.email,
            "password": request.password,
            "connection": self.connection,
            "email_verified": False,
            "given_name": request.given_name,
            "family_name": request.family_name,
            "user_metadata": {"locale": request.locale} if request.locale else {}
        }
        try:
            user = api.users.create(user_data)
            return normalize_auth0_user_payload(user)
        except Auth0Error as e:
            raise Exception(f"Auth0 registration failed: {e}")

    def login(self, request: LoginRequest) -> LoginResponse:
        from auth0.v3.authentication import Database
        db = Database(self.domain)
        try:
            token = db.login(
                client_id=self.client_id,
                client_secret=self.client_secret,
                username=request.email,
                password=request.password,
                realm=self.connection,
                audience=self.audience,
                scope="openid profile email offline_access"
            )
            return normalize_auth0_token_payload(token)
        except Auth0Error as e:
            raise Exception(f"Auth0 login failed: {e}")

    def refresh_session(self, request: RefreshSessionRequest) -> RefreshSessionResponse:
        from auth0.v3.authentication import GetToken
        get_token = GetToken(self.domain)
        try:
            token = get_token.refresh_token(
                client_id=self.client_id,
                client_secret=self.client_secret,
                refresh_token=request.refresh_token
            )
            return RefreshSessionResponse(
                access_token=token["access_token"],
                expires_in=token["expires_in"],
                token_type=token["token_type"]
            )
        except Auth0Error as e:
            raise Exception(f"Auth0 refresh failed: {e}")

    def initiate_password_reset(self, request: PasswordResetRequest) -> PasswordResetResponse:
        from auth0.v3.authentication import Database
        db = Database(self.domain)
        try:
            result = db.change_password(
                client_id=self.client_id,
                email=request.email,
                connection=self.connection
            )
            return PasswordResetResponse(
                reset_initiated=True,
                message=result.get("message", "Password reset email sent.")
            )
        except Auth0Error as e:
            raise Exception(f"Auth0 password reset failed: {e}")