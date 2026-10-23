import os


def get_dd_api_key() -> str:
    """Return Datadog API key from environment."""
    return os.getenv("DD_API_KEY")


def get_ibm_cloud_api_key() -> str:
    """Return IBM Cloud API key from environment."""
    return os.getenv("IBM_CLOUD_API_KEY")


def get_ibm_logs_instance_id() -> str:
    """Return IBM Cloud Logs instance ID from environment."""
    return os.getenv("IBM_LOGS_INSTANCE_ID")


def get_azure_tenant_id() -> str:
    """Return Azure tenant ID from environment."""
    return os.getenv("AZURE_TENANT_ID")


def get_azure_client_id() -> str:
    """Return Azure client ID (access token) from environment."""
    return os.getenv("AZURE_CLIENT_ID")


def get_aws_access_key_id() -> str:
    """Return AWS access key from environment."""
    return os.getenv("AWS_ACCESS_KEY_ID")


def get_aws_secret_access_key() -> str:
    """Return AWS secret key from environment."""
    return os.getenv("AWS_SECRET_ACCESS_KEY")
