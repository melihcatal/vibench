import os
import boto3
from botocore.exceptions import ClientError

from identity_models import (
    UserRegisterRequest,
    TokenResponse,
    RefreshSessionRequest,
    RefreshSessionResponse,
    StartPasswordResetRequest,
    ConfirmPasswordResetRequest,
)


class IdentityClient:
    """Unified client wrapper for Amazon Cognito User Pools operations."""

    def __init__(self, *, region: str, user_pool_id: str, client_id: str, identity_pool_id: str = None):
        self.region = region
        self.user_pool_id = user_pool_id
        self.client_id = client_id
        self.identity_pool_id = identity_pool_id
        self.client = boto3.client(
            'cognito-idp',
            region_name=self.region,
        )

    def register_user(self, request: UserRegisterRequest) -> dict:
        """Register a new user via Cognito Admin API."""
        payload = {
            'UserPoolId': self.user_pool_id,
            'ClientId': self.client_id,
            'Username': request.username,
            'Password': request.password,
        }
        # Append custom attributes if provided
        if request.user_attributes:
            payload['UserAttributes'] = [
                {'Name': key, 'Value': value} for key, value in request.user_attributes.items()
            ]
        try:
            response = self.client.admin_create_user(**payload)
            return response
        except ClientError as e:
            raise RuntimeError(f"Cognito registration failed: {e}")

    def login(self, email: str, password: str) -> TokenResponse:
        """Authenticate a user with email/password and return tokens."""
        try:
            auth_response = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={'USERNAME': email, 'PASSWORD': password},
            )
            # Cognito returns AccessToken, IdToken, RefreshToken in the response
            return TokenResponse(
                access_token=auth_response['AuthenticationResult']['AccessToken'],
                id_token=auth_response['AuthenticationResult']['IdToken'],
                refresh_token=auth_response['AuthenticationResult']['RefreshToken'],
            )
        except ClientError as e:
            raise RuntimeError(f"Cognito login failed: {e}")

    def refresh_session(self, refresh_token: str) -> RefreshSessionResponse:
        """Use a refresh token to get a new set of tokens."""
        try:
            auth_response = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='REFRESH_TOKEN_AUTH',
                AuthParameters={'REFRESH_TOKEN': refresh_token},
            )
            return RefreshSessionResponse(**auth_response['AuthenticationResult'])
        except ClientError as e:
            raise RuntimeError(f"Cognito refresh failed: {e}")

    def start_password_reset(self, email: str) -> None:
        """Start password reset flow for a given email."""
        try:
            self.client.forgot_password(
                ClientId=self.client_id,
                Username=email,
            )
        except ClientError as e:
            raise RuntimeError(f"Cognito forgot password failed: {e}")

    def confirm_password_reset(self, email: str, confirmation_code: str, new_password: str) -> None:
        """Confirm the reset code and set new password."""
        try:
            self.client.confirm_forgot_password(
                ClientId=self.client_id,
                Username=email,
                ConfirmationCode=confirmation_code,
                Password=new_password,
            )
        except ClientError as e:
            raise RuntimeError(f"Cognito confirm forgot password failed: {e}")
