# security_client.py
import os
from typing import Any, Dict

# Example: configuration via environment variables
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
VAULT_ADDR = os.getenv('VAULT_ADDR', 'http://127.0.0.1:8200')
VAULT_TOKEN = os.getenv('VAULT_TOKEN')
# Optional: path to a credentials file for Google Cloud
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Helper to obtain the appropriate client depending on the backend you want to use
# In a real project you might dispatch based on a config flag.

def get_secret_manager_client() -> Any:
    """Return a configured client for a secret management backend.

    This stub returns an AWS Secrets Manager client for demonstration.
    Replace with Vault or Google Secret Manager imports as needed.
    """
    import boto3  # type: ignore
    return boto3.client('secretsmanager', region_name=AWS_REGION)
```