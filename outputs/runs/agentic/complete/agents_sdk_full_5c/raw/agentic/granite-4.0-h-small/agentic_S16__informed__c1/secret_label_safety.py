import os
from ibm_secrets_manager_sdk import SecretsManagerV1
from security_models import SecretSpec, SecretResponse

def secret_label_safety(secret_id, label_field='label'):
    """Checks a secret's label/note for unsafe text.
    Returns:
        bool: True if safe, False otherwise.
    """
    api_key = os.getenv('IBM_SECRETS_MANAGER_APIKEY')
    if not api_key:
        raise RuntimeError('IBM_SECRETS_MANAGER_APIKEY not set')
    client = SecretsManagerV1.new_instance(api_key=api_key)
    secret = client.get_secret(secret_id=secret_id).get_result()
    payload = secret.get('secret_data', '')
    import json
    data = json.loads(payload)
    label = data.get(label_field, '')
    # Simple unsafe word check (placeholder for real moderation)
    unsafe_words = {'password', 'secret', 'private'}
    return not any(word in label.lower() for word in unsafe_words)
