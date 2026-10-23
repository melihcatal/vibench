import os
import boto3
from botocore.exceptions import ClientError
from typing import Any, Dict

# AWS KMS client wrapper for the scoring task

class KmsClient:
    """Thin wrapper around boto3 KMS that provides high‑level request/response objects
    compatible with the local security_models definitions."""

    def __init__(self):
        # Uses the AWS credentials from environment (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)
        self._client = boto3.client('kms')

    def encrypt(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Calls AWS KMS Encrypt and returns the raw response."""
        return self._client.encrypt(**request)

    def decrypt(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calls AWS KMS Decrypt and returns the raw response.
        """
        return self._client.decrypt(**request)

    def generate_data_key(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calls GenerateDataKey (for envelope encryption) and returns raw response.
        """
        return self._client.generate_data_key(**request)

    def sign(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calls Sign (RSA/ECC keys) and returns the raw response.
        """
        return self._client.sign(**request)

    def verify(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calls Verify (RSA/ECC keys) and returns the raw response.
        """
        return self._client.verify(**request)

    def _handle_error(self, e: ClientError) -> None:
        print(f"AWS KMS error {e.response['Error']['Code']}: {e.response['Error']['Message']}")
        raise e

    def __getattr__(self, name: str):
        # Delegate any missing attribute to the underlying boto3 client for future API coverage
        return getattr(self._client, name)

# Example helper to normalise boto3 response into a local model class (placeholder)
def _to_local_model(response: Dict[str, Any], model_class: Any) -> Any:
    # In real code, map boto3 fields to model fields; here we just return a dummy
    return model_class(**response)

# Export the class for import by the scoring files
__all__ = ['KmsClient']
