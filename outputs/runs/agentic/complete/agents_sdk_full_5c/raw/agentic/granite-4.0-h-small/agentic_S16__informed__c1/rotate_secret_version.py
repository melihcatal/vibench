import os
from ibm_secrets_manager_sdk import SecretsManagerV1

def rotate_secret_version(secret_id, version):
    """Reads a specific version (or staged) of a secret from IBM Cloud Secrets Manager.
    Args:
        secret_id (str): Identifier of the secret.
        version (str): Version identifier, e.g., a version number or 'staged'.
    Returns:
        dict: The secret payload for the requested version.
    Raises:
        Exception: On failure to retrieve the secret.
    """
    api_key = os.getenv('IBM_SECRETS_MANAGER_APIKEY')
    if not api_key:
        raise RuntimeError('IBM_SECRETS_MANAGER_APIKEY environment variable not set')
    client = SecretsManagerV1.new_instance(api_key=api_key)
    # Use the version identifier in the request
    response = client.get_secret(secret_id=secret_id, version=version)
    data = response.get_result()
    return data.get('secret_data')
