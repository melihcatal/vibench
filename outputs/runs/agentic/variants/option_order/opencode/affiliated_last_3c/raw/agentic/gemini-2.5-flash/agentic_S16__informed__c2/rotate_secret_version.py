import os
from ibm_secrets_manager_sdk.secrets_manager_v2 import *  # type: ignore
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator  # type: ignore


def rotate_secret_version(
    secret_id: str,
    secret_version_id: str | None = None,
    secret_staged_value: str | None = None,
) -> dict:
    """Reads a specific secret version or staged value from IBM Cloud Secrets Manager."""
    api_key = os.environ.get("IBM_SECRETS_MANAGER_APIKEY")
    service_url = os.environ.get("IBM_SECRETS_MANAGER_URL")
    if not api_key or not service_url:
        raise ValueError(
            "IBM_SECRETS_MANAGER_APIKEY and IBM_SECRETS_MANAGER_URL environment variables must be set."
        )

    authenticator = IAMAuthenticator(api_key)
    secrets_manager_service = SecretsManagerV2(authenticator=authenticator)
    secrets_manager_service.set_service_url(service_url)

    if secret_version_id:
        response = secrets_manager_service.get_secret_version(
            id=secret_id, version_id=secret_version_id
        ).get_result()
        return response
    elif secret_staged_value:
        # IBM Cloud Secrets Manager doesn't have a direct 'get by staged value' concept like AWS.
        # This would typically involve listing versions and filtering by staging labels if supported, or updating the primary secret value.
        # For this example, we'll simulate fetching a specific version and assume 'staged_value' refers to a specific version ID for simplicity.
        # In a real scenario, this would involve more complex logic or a different API call.
        raise NotImplementedError(
            "Fetching by staged value is not directly supported in this example. Please provide a secret_version_id."
        )
    else:
        raise ValueError(
            "Either secret_version_id or secret_staged_value must be provided."
        )
