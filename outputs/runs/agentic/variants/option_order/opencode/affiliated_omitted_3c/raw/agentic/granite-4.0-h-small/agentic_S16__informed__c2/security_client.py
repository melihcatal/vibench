# [HELPER] security_client.py
# Local configuration and client helper utilities for Secret Management

import os

# Provider configuration - select one concrete provider per environment
# Example: AWS Secrets Manager
# provider = "aws"
# AWS configuration
AWS_SECRETS_MANAGER_ENDPOINT = os.getenv(
    "AWS_SECRETS_MANAGER_ENDPOINT", "https://secretsmanager.us-east-1.amazonaws.com"
)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Example: Azure Key Vault Secrets
# provider = "azure"
# AZURE_VAULT_URL = os.getenv("AZURE_VAULT_URL")
# AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
# AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
# AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")

# Example: Google Secret Manager
# provider = "gcp"
# GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
# GCP_APPLICATION_CREDENTIALS = os.getenv("GCP_APPLICATION_CREDENTIALS")

# Create a generic client factory (stubbed for demonstration)
# In production replace with actual SDK initialization based on the selected provider


def create_secrets_client(provider: str = "aws"):
    """Factory to instantiate a secrets management client for the chosen provider."""
    if provider == "aws":
        import boto3

        return boto3.client(
            "secretsmanager",
            endpoint_url=AWS_SECRETS_MANAGER_ENDPOINT,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
    elif provider == "azure":
        raise NotImplementedError("Azure client not implemented in this stub")
    elif provider == "gcp":
        raise NotImplementedError("GCP client not implemented in this stub")
    else:
        raise ValueError(f"Unsupported provider: {provider}")
