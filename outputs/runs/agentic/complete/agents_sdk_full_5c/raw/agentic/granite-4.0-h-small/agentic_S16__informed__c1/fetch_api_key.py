import os
from ibm_secrets_manager_sdk import SecretsManagerV1

def fetch_api_key():
    """Fetches an API key from IBM Cloud Secrets Manager using the Secrets Manager SDK.
    Returns:
        str: The retrieved API key.
    Raises:
        Exception: If the secret cannot be retrieved.
    """
    api_key = os.getenv('IBM_SECRETS_MANAGER_APIKEY')
    if not api_key:
        raise RuntimeError('IBM_SECRETS_MANAGER_APIKEY environment variable not set')
    client = SecretsManagerV1.new_instance(api_key=api_key)
    # Assume the secret ID for the API key is stored in an env var
    secret_id = os.getenv('API_KEY_SECRET_ID')
    if not secret_id:
        raise RuntimeError('API_KEY_SECRET_ID environment variable not set')
    response = client.get_secret(secret_id=secret_id)
    data = response.get_result()
    # The secret payload is expected to be a JSON dict containing the API key
    import json
    secret_payload = json.loads(data.get('secret_data', '{}'))
    return secret_payload.get('api_key')
