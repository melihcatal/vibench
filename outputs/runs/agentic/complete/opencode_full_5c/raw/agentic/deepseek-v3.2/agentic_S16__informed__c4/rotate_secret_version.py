import os
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_secrets_manager_sdk.secrets_manager_v2 import SecretsManagerV2


def rotate_secret_version(secret_id: str, version_id: str = None) -> str:
    """Read a specific secret version or staged value from IBM Cloud Secrets Manager."""
    api_key = os.environ.get("IBM_SECRETS_MANAGER_APIKEY")
    instance_id = os.environ.get("IBM_SECRETS_MANAGER_INSTANCE_ID")

    if not api_key:
        raise ValueError("IBM_SECRETS_MANAGER_APIKEY environment variable must be set")
    if not instance_id:
        raise ValueError(
            "IBM_SECRETS_MANAGER_INSTANCE_ID environment variable must be set"
        )

    authenticator = IAMAuthenticator(apikey=api_key)
    secrets_manager = SecretsManagerV2(authenticator=authenticator)
    secrets_manager.set_service_url(
        "https://api.us-south.secrets-manager.cloud.ibm.com"
    )

    if version_id:
        response = secrets_manager.get_secret_version(
            secret_id=secret_id, id=version_id
        )
    else:
        response = secrets_manager.get_secret(id=secret_id)

    secret_data = response.get_result()
    return secret_data.get("payload", "")
