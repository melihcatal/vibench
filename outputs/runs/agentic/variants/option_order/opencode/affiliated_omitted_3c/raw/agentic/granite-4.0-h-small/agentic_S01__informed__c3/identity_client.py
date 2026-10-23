import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError


class IdentityClient:
    """Local helper utilities for Email/Password Account Lifecycle.

    Centralizes configuration and authentication for Cognito API calls.
    """

    def __init__(self):
        self.cognito = boto3.client(
            "cognito-idp",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def _handle_error(self, e):
        if isinstance(e, ClientError):
            err = e.response["Error"]["Message"]
        else:
            err = str(e)
        raise RuntimeError(f"Identity API error: {err}")

    def confirm_sign_up(self, username: str):
        try:
            self.cognito.admin_confirm_sign_up(
                UserPoolId=os.getenv("COGNITO_POOL_ID"), Username=username
            )
        except (BotoCoreError, ClientError) as e:
            self._handle_error(e)

    def get_user_attributes(self, username: str):
        try:
            return self.cognito.admin_get_user(
                UserPoolId=os.getenv("COGNITO_POOL_ID"), Username=username
            )["UserAttributes"]
        except (BotoCoreError, ClientError) as e:
            self._handle_error(e)
