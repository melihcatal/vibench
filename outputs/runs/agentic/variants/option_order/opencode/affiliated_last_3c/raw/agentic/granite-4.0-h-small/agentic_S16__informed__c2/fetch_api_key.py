import os
from ibm_secrets_manager_sdk import SecretsManagerV1


def fetch_api_key(secret_name: str) -> str:
    """Fetch an API key from IBM Cloud Secrets Manager.
    Args:
        secret_name: Name of the secret holding the API key.
    Returns:
        The retrieved API key value.
    """
    api_key = os.getenv("IBM_SECRETS_MANAGER_APIKEY")
    service_url = os.getenv("IBM_SECRETS_MANAGER_URL")
    client = SecretsManagerV1.new_instance(api_key=api_key, service_url=service_url)
    response = client.get_secret(
        secret_type="arbitrary",
        id=secret_name,
    ).get_result()
    # Assuming the secret value is a JSON string with {"api_key": "value"}
    import json

    secret_data = json.loads(response.get("plaintext", {}))
    return secret_data.get("api_key")
