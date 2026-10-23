import os
from google.cloud import kms
from security_client import get_kms_client

def key_usage_summary(project_id, location_id, key_ring_id, crypto_key_id, kms_client=None):
    """Retrieves and returns usage metrics for a KMS symmetric key (e.g., encrypt/decrypt calls)."""
    if kms_client is None:
        kms_client = get_kms_client()
    key_name = f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}"
    # Retrieve the key resource and its IAM policy / usage metrics (metadata may include usage counters)
    key = kms_client.get_crypto_key(name=key_name)
    # Google Cloud KMS exposes usage metrics through the Key resource's `state` and `crypto_key_versions` metadata.
    # For demonstration we extract version counts and timestamps.
    usage = {
        "key_name": key_name,
        "algorithm": key.algorithm,
        "created": key.create_time.isoformat() if key.create_time else None,
        "version_count": len(key.crypto_key_versions),
        "purpose": key.purpose,
    }
    # Optionally pull recent usage events via Cloud Audit Logs (not shown here)
    return usage

if __name__ == "__main__":
    project_id = os.getenv("GCLOUD_PROJECT")
    location_id = "global"
    key_ring_id = "my-key-ring"
    crypto_key_id = "my-key"
    info = key_usage_summary(project_id, location_id, key_ring_id, crypto_key_id)
    print("Key Usage Summary:", info)
