import os
import boto3
from typing import Any

# Public factory returning the appropriate concrete SecretClient for the configured provider.
# The implementation here defaults to AWS Secrets Manager, but can be swapped via env vars.

def create_secret_client() -> Any:
    """Factory for a SecretClient implementation based on runtime configuration.

    Returns an object conforming to the SecretClient protocol defined in security_client.py.
    """
    # Pick provider from environment; new providers can be added here.
    provider = os.getenv('SECRET_MANAGER_PROVIDER', 'aws')
    if provider == 'aws':
        return AWSSecretClient()
    raise ValueError(f'Unsupported provider: {provider}')
