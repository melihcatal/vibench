import json
from typing import Any, Dict


def parse_json_secret(secret_id: str, secret_version: str = "latest") -> Dict[str, Any]:
    """Retrieve and parse a JSON-formatted secret from IBM Cloud Secrets Manager.

    Args:
        secret_id (str): UUID of the secret.
        secret_version (str): Version identifier (default \"latest\").

    Returns:
        Dict containing the parsed JSON data.

    Raises:
        RuntimeError: If the secret cannot be fetched or is not valid JSON.
    """
    from ibm_secrets_manager_sdk import SecretsManagerV1
    from ibm_secrets_manager_sdk.integrations.client_factory import ClientFactory
    import os

    service = ClientFactory.create_service(SecretsManagerV1, "secrets-manager", endpoint="https://us-south.secrets-manager.appdomain.cloud")
    service.set_apikey(os.getenv("IBM_SECRETS_MANAGER_APIKEY"))

    version = service.get_secret_version(secret_id=secret_id, version_id=secret_version)
    payload = version.get_result().get_result()

    try:
        return json.loads(payload)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Secret {secret_id}:{secret_version} is not valid JSON") from exc
