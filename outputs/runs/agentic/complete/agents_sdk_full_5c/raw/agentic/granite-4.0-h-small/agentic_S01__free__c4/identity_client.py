import boto3
from botocore.config import Config

class IdentityClient:
    """Local thin wrapper around AWS SDK clients for the Email/Password lifecycle.",
    
    Provides a uniform interface for Cognito admin actions (create_user, init_auth,
    refresh_token, forgot_password). In production the underlying boto3 client is
    replaced by a real provider SDK; this wrapper keeps credential handling and
    request/response normalization in one place.
    """
    def __init__(self, service: str, region_name: str, aws_access_key_id: str, aws_secret_access_key: str):
        self.service = service
        self.region_name = region_name
        self.credentials = {
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
        }
        self.config = Config(retries={"max_attempts": 5})
        self._client = None

    @property
    def _client(self):
        if not hasattr(self, "_raw_client"):
            self._raw_client = boto3.client(
                self.service,
                region_name=self.region_name,
                **self.credentials,
                config=self.config
            )
        return self._raw_client

    def __getattr__(self, name):
        # Delegate unknown methods to the underlying boto3 client for flexibility.
        return getattr(self._client, name)
