# key_usage_summary.py
import json
from google.cloud import kms_v1
from security_client import KmsClient

def summarize_key_usage(project_id: str, key_ring: str, crypto_key: str) -> dict:
    """Summarizes usage metrics for a Cloud KMS CryptoKey.

    Args:
        project_id (str): GCP project id.
        key_ring (str): Key ring name.
        crypto_key (str): Crypto key name (without full resource prefix).

    Returns:
        dict: Summary containing creation time, rotations, and usage counts.
    """
    client = KmsClient.get_instance()
    name = client.crypto_key_path(project_id, key_ring, crypto_key)
    # Retrieve key resource (usage metrics are in the policy, not in the CryptoKey object directly)
    key = client.get_crypto_key(name)
    summary = {
        'name': name,
        'created': key.create_time.isoformat() if key.create_time else None,
        'rotations': [_rot.isoformat() for _rot in key.rotation_history],
        'usage': {
            'encrypt_count': None,
            'decrypt_count': None,
            'sign_count': None,
            'verify_count': None,
        },
    }
    # NOTE: Google KMS does not expose per-operation counters via the API; this placeholder
    # would be filled by an audit log export (e.g., Cloud Logging) in production.
    return summary
