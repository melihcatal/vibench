from security_client import get_secret_client
from ibm_secrets_manager_sdk.models import SecretMetadata

NON_SENSITIVE_LABELS = {'environment', 'owner', 'team'}

UNSAFE_PATTERNS = {
    'password': 'password',
    'key': 'key',
    'token': 'token'
}

def are_labels_safe(metadata: SecretMetadata) -> bool:
    """Return True if secret labels contain no unsafe terms.

    Uses the same keyword check as secret_label_safety.py.
    """
    for label in metadata.get('labels', {}).keys():
        label_low = label.lower()
        for term in UNSAFE_PATTERNS.keys():
            if term in label_low:
                return False
    return True

# Demo usage
if __name__ == "__main__":
    client = get_secret_client()
    secret = client.get_secret(secret_name='my-secret').get_result()
    safe = are_labels_safe(secret.get('metadata', {}))
    print('Labels safe?', safe)