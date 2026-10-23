import os
from azure.identity import DefaultAzureCredential, ClientSecretCredential

def get_aws_credentials():
    """Fetches AWS credentials from environment variables."""
    return {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    }

def get_doppler_token():
    """Fetches Doppler token from environment variables."""
    return os.getenv("DOPPLER_TOKEN")

def get_google_project_id():
    """Fetches Google Cloud Project ID from environment variables."""
    return os.getenv("GOOGLE_CLOUD_PROJECT")


def get_azure_credential():
    """
    Provides a credential object for Azure SDKs.
    Tries ClientSecretCredential first, then falls back to DefaultAzureCredential.
    """
    try:
        return ClientSecretCredential(
            tenant_id=os.environ["AZURE_TENANT_ID"],
            client_id=os.environ["AZURE_CLIENT_ID"],
            client_secret=os.environ["AZURE_CLIENT_SECRET"],
        )
    except KeyError:
        # Fallback for other auth methods like managed identity, CLI login
        return DefaultAzureCredential()
