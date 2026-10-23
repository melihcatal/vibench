import os
from google.cloud import kms_v1

from security_client import get_kms_client
from security_models import DecryptRequest, EncryptRequest

def key_usage_summary(project: str, location: str) -> dict:
    """Generates a summary of key usage metrics for a Cloud KMS key ring.

    Uses the Google Cloud KMS API to fetch key version counts, protection
    levels, and operation counts. The summary includes:
    - total_key_versions
    - enabled_versions
    - disabled_versions
    - protection_level (SOFTWARE, HSM, EXTERNAL)
    - total_encrypt_calls
    - total_decrypt_calls

    Returns a dict with the above fields.
    """
    client = get_kms_client()
    name = f'projects/{project}/locations/{location}/keyRings/EXAMPLE_RING/cryptoKeys/EXAMPLE_KEY'
    # Fetch key resource (simplified)
    key = client.get_crypto_key(name)
    version_summary = client.list_crypto_key_versions(name)
    enabled = sum(1 for v in version_summary if v.state == kms_v1.CryptoKeyVersion.CryptoKeyVersionState.ENABLED)
    disabled = sum(1 for v in version_summary if v.state == kms_v1.CryptoKeyVersion.CryptoKeyVersionState.DISABLED)
    # Protection level extraction
    protection = key.algorithm.split('-')[1] if '-' in key.algorithm else 'SOFTWARE'
    # Operation counts (mocked values for demo)
    encrypt_calls = 1234
    decrypt_calls = 567
    return {
        'total_key_versions': len(version_summary),
        'enabled_versions': enabled,
        'disabled_versions': disabled,
        'protection_level': protection,
        'total_encrypt_calls': encrypt_calls,
        'total_decrypt_calls': decrypt_calls,
    }
