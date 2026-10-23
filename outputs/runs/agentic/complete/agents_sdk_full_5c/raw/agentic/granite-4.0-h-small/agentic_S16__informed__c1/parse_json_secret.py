import os
from ibm_secrets_manager_sdk import SecretsManagerV1
import json

def parse_json_secret(secret_id):
    """Retrieves a secret identified by `secret_id` and parses its JSON payload.
    Args:
        secret_id (str): The secret identifier in Secrets Manager.
    Returns:
        dict: Parsed JSON data from the secret.
    Raises:
        Exception: If retrieval or parsing fails.
    """
    api_key = os.getenv('IBM_SECRETS_MANAGER_APIKEY')
    if not api_key:
        raise RuntimeError('IBM_SECRETS_MANAGER_APIKEY environment variable not set')
    client = SecretsManagerV1.new_instance(api_key=api_key)
    response = client.get_secret(secret_id=secret_id)
    data = response.get_result()
    # The secret payload is stored under 'secret_data' as a JSON string
    payload_str = data.get('secret_data', '')
    return json.loads(payload_str)
