# security_client.py
# [HELPER]
# Local configuration and client helper utilities for Secret Management

import os
from typing import Dict, Any

# --- Provider selection via environment variables ---
PROVIDER = os.getenv("SECRET_MANAGER_PROVIDER", "aws")  # default to AWS

# --- Provider-specific configuration defaults ---
if PROVIDER == "aws":
    AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    client_factory = lambda: boto3.client(
        "secretsmanager",
        region_name=AWS_REGION,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
elif PROVIDER == "ibm":
    IBM_APIKEY = os.getenv("IBM_SECRETS_MANAGER_APIKEY")
    client_factory = lambda: SecretsManagerV1.new_instance(
        authenticator="iam", apikey=IBM_APIKEY
    )
    # set service URL after instance creation if needed
else:
    raise ValueError(f"Unsupported provider: {PROVIDER}")


def get_client() -> Any:
    """Instantiate and return the appropriate secret manager client based on the configured provider.

    Returns:
        A configured client object ready for secret operations.
    """
    return client_factory()
