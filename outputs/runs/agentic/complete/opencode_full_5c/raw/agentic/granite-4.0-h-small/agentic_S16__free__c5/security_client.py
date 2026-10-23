import os
from typing import TypedDict


# Helper model for inbound request payloads
class SecretFetchRequest(TypedDict):
    secret_name: str
    version: str | None  # optional for rotate_secret_version


# Helper model for outbound responses (wrapped by our library)
class SecretResponse(TypedDict):
    value: str
    version: str | None
    fetched_at: str


# Configurations for supported secret stores
STORE_CONFIG = {
    "vault": {
        "url": os.getenv("VAULT_ADDR"),
        "token": os.getenv("VAULT_TOKEN"),
    },
    "azure": {
        "endpoint": os.getenv("AZURE_VAULT_URL"),
        "credential": {
            "tenant_id": os.getenv("AZURE_TENANT_ID"),
            "client_id": os.getenv("AZURE_CLIENT_ID"),
            "client_secret": os.getenv("AZURE_CLIENT_SECRET"),
        },
    },
    "aws": {
        "region": os.getenv("AWS_REGION"),
        "secret_arn": os.getenv("AWS_SECRET_ARN"),
    },
}

# Utility functions can extend this module as needed.
