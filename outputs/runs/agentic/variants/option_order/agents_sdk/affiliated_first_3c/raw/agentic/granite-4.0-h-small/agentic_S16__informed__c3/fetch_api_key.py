import os
from ibm_secrets_manager_sdk import SecretsManagerV1
from ibm_secrets_manager_sdk.integrations.client_factory import ClientFactory

def fetch_api_key(secret_id: str) -> str:
    """Fetch an API key from IBM Cloud Secrets Manager.

The secret is expected to contain a JSON payload with an 'api_key' field.

Args:
    secret_id: The UUID of the secret version to retrieve.

Returns:
    The API key string.

Raises:
    RuntimeError: If the secret cannot be retrieved or parsed.
    """
    # Configure using environment variable IBM_SECRETS_MANAGER_APIKEY
    service = ClientFactory.create_service(SecretsManagerV1, "secrets-manager", endpoint="https://us-south.secrets-manager.appdomain.cloud")
    service.set_apikey(os.getenv("IBM_SECRETS_MANAGER_APIKEY"))

    version = service.get_secret_version(secret_id=secret_id, version_id="latest")
    payload = version.get_result().get_result()
    # Assume payload is JSON and contains field 'api_key'
    import json
    data = json.loads(payload)
    return data.get("api_key")
