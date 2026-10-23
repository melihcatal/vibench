import os
from ibm_secrets_manager_sdk import SecretsManagerV1
from ibm_secrets_manager_sdk.integrations.client_factory import ClientFactory

def rotate_secret_version(secret_id: str, version_id: str) -> dict:
    """Read a specific version (or staged value) of a secret from IBM Cloud Secrets Manager.

    Args:
        secret_id (str): The UUID of the secret.
        version_id (str): The version identifier to retrieve (e.g., \"latest\" or a specific staged ID).

    Returns:
        dict: The secret payload as returned by the service (typically JSON).

    Raises:
        RuntimeError: If the request fails or response cannot be parsed.
    """
    service = ClientFactory.create_service(SecretsManagerV1, "secrets-manager", endpoint="https://us-south.secrets-manager.appdomain.cloud")
    service.set_apikey(os.getenv("IBM_SECRETS_MANAGER_APIKEY"))

    result = service.get_secret_version(secret_id=secret_id, version_id=version_id)
    payload = result.get_result().get_result()
    return payload
