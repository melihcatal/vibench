import boto3
import os
from typing import Optional

class AWSSecretsManagerClient:
    """Client helper for AWS Secrets Manager."""

    def __init__(self, region_name: Optional[str] = None):
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
        self._client = boto3.client('secretsmanager', region_name=self.region_name)

    def get_secret(self, secret_id: str, version_stage: str = "AWSCURRENT") -> str:
        """Fetches a secret by its ID and optional version stage."""
        try:
            get_secret_value_response = self._client.get_secret_value(
                SecretId=secret_id,
                VersionStage=version_stage
            )
            if 'SecretString' in get_secret_value_response:
                return get_secret_value_response['SecretString']
            else:
                return get_secret_value_response['SecretBinary'].decode('utf-8')
        except self._client.exceptions.ResourceNotFoundException:
            raise ValueError(f"Secret '{secret_id}' not found.")
        except Exception as e:
            raise RuntimeError(f"Error fetching secret '{secret_id}': {e}")

