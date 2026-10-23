# security_client.py
import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError

from security_models import SecretValueResult, SecretMetadataResult

class SecretManagerClient:
    """Thin wrapper around AWS Secrets Manager client that centralizes configuration.

    All methods return data consistent with the local response models defined in security_models.
    """
    def __init__(self):
        # By default we rely on the environment variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY,
        # or an AWS profile configured via the boto3 credential chain.
        self.client = boto3.client('secretsmanager')

    def get_secret_value(self, secret_id: str, version_stage: str = 'AWSCURRENT') -> SecretValueResult:
        """Fetch the plaintext value of a secret.

        Returns a SecretValueResult object with the secret string and optional metadata.
        """
        try:
            resp = self.client.get_secret_value(SecretId=secret_id, VersionStage=version_stage)
        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError(f'Failed to retrieve secret {secret_id}: {exc}')
        # AWS may return SecretBinary or SecretString based on how the secret was stored.
        value = resp.get('SecretString') or resp.get('SecretBinary')
        return SecretValueResult(value=value, metadata=resp)

    def get_secret_metadata(self, secret_id: str) -> SecretMetadataResult:
        """Retrieve metadata (e.g., description, last updated time) without returning the secret value.

        This uses the DescribeSecret API which does not expose secret contents.
        """
        try:
            resp = self.client.describe_secret(SecretId=secret_id)
        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError(f'Failed to describe secret {secret_id}: {exc}')
        return SecretMetadataResult(**resp)

    def list_secrets(self) -> list[SecretMetadataResult]:
        """List brief information about all secrets in the account.

        Returns a list of SecretMetadataResult objects.
        """
        try:
            resp = self.client.list_secrets()
        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError(f'Failed to list secrets: {exc}')
        return [SecretMetadataResult(**item) for item in resp.get('SecretList', [])]

    def rotate_secret(self, secret_id: str) -> None:
        """Trigger a secret rotation (if a rotation Lambda is attached).

        This operation is async; it starts the rotation workflow.
        """
        try:
            self.client.rotate_secret(SecretId=secret_id)
        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError(f'Rotation failed for secret {secret_id}: {exc}')

    def update_secret(self, secret_id: str, secret_string: str) -> None:
        """Update a secret with new plaintext data.

        Use when you have generated a new value locally.
        """
        try:
            self.client.put_secret_value(SecretId=secret_id, SecretString=secret_string)
        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError(f'Update failed for secret {secret_id}: {exc}')