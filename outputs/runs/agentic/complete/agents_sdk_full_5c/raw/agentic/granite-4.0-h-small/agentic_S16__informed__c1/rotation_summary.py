import os
from ibm_secrets_manager_sdk import SecretsManagerV1
from security_models import SecretSpec, SecretResponse

def rotation_summary(secret_id, version):
    """Summarizes rotation status for a secret after reading a specific version.
    Args:
        secret_id (str): Identifier of the secret.
        version (str): Version to inspect (e.g., number or 'staged').
    Returns:
        dict: Summary containing version, timestamp, and required fields checklist.
    """
    api_key = os.getenv('IBM_SECRETS_MANAGER_APIKEY')
    if not api_key:
        raise RuntimeError('IBM_SECRETS_MANAGER_APIKEY not set')
    client = SecretsManagerV1.new_instance(api_key=api_key)
    resp = client.get_secret(secret_id=secret_id, version=version)
    raw = resp.get_result()
    payload = raw.get('secret_data', '')
    import json
    data = json.loads(payload)
    summary = {
        'secret_id': secret_id,
        'retrieved_version': version,
        'retrieved_at': raw.get('created_at', ''),
        'fields_present': list(data.keys())
    }
    return summary
