import os
import boto3
from botocore.exceptions import ClientError

class SecretsManagerClient:
    """A helper class to manage AWS Secrets Manager client."""

    def __init__(self, region_name: str = None):
        self.region_name = region_name if region_name else os.environ.get("AWS_REGION", "us-east-1")
        self._client = None

    def get_client(self):
        """Returns an initialized boto3 Secrets Manager client."""
        if self._client is None:
            session = boto3.session.Session()
            self._client = session.client(
                service_name='secretsmanager',
                region_name=self.region_name
            )
        return self._client


def get_aws_secrets_manager_client():
    """Factory function to get a pre-configured AWS Secrets Manager client."""
    return SecretsManagerClient().get_client()

