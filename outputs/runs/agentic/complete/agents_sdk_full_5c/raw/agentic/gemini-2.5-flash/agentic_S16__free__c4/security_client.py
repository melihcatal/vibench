import boto3
import os

class SecretsManagerClient:
    """
    A helper client for interacting with AWS Secrets Manager.
    Encapsulates client initialization and common configurations.
    """
    def __init__(self, region_name: str = None):
        if region_name is None:
            self.region_name = os.environ.get("AWS_REGION", "us-east-1")
        else:
            self.region_name = region_name
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = boto3.client("secretsmanager", region_name=self.region_name)
        return self._client

