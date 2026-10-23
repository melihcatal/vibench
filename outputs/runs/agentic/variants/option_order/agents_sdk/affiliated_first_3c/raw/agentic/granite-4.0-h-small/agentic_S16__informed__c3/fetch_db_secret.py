import os
from ibm_secrets_manager_sdk import SecretsManagerV1
from ibm_secrets_manager_sdk.integrations.client_factory import ClientFactory

def fetch_db_secret(secret_id: str) -> dict:
    """Fetch a database connection secret from IBM Cloud Secrets Manager.

The secret is expected to contain a JSON payload with typical DB connection fields
such as username, password, host, port, and dbname.

Args:
    secret_id: The UUID of the secret version to retrieve.

Returns:
    Dict mapping field names to values.

Raises:
    RuntimeError: If retrieval or parsing fails.
    """
    service = ClientFactory.create_service(SecretsManagerV1, "secrets-manager", endpoint="https://us-south.secrets-manager.appdomain.cloud")
    service.set_apikey(os.getenv("IBM_SECRETS_MANAGER_APIKEY"))

    version = service.get_secret_version(secret_id=secret_id, version_id="latest")
    payload = version.get_result().get_result()
    import json
    return json.loads(payload)
