import boto3
import os

class IdentityClient:
    def __init__(self):
        # Load AWS credentials from environment variables
        self.aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        # Basic configuration for the Cognito service
        self.config = {
            'user_pool_id': os.getenv('COGNITO_USER_POOL_ID'),
            'client_id': os.getenv('COGNITO_CLIENT_ID')
        }
        # Create the low-level Cognito Identity Provider client
        self.cognito_provider = boto3.client(
            'cognito-idp',
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=self.region
        )
        # Create the high‑level Cognito Identity client for admin actions
        self.cognito_admin = boto3.client(
            'cognito-idp',
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=self.region
        )

    def cognito_admin_create_user(self, **kwargs):
        return self.cognito_admin.admin_create_user(**kwargs)

    def cognito_admin_reset_user_password(self, **kwargs):
        return self.cognito_admin.admin_reset_user_password(**kwargs)

    def cognito_initiate_auth(self, **kwargs):
        return self.cognito_provider.initiate_auth(**kwargs)

    def cognito_refresh_token(self, **kwargs):
        return self.cognito_provider.refresh_token(**kwargs)
