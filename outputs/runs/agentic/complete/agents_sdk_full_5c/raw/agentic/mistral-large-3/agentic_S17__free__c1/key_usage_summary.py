from google.cloud import kms
from security_client import get_kms_client
from typing import List, Dict

def summarize_key_usage(project_id: str, location_id: str, key_ring_id: str, key_id: str) -> Dict[str, int]:
    client = get_kms_client()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Fetch key versions and their usage metrics
    versions = client.list_crypto_key_versions(request={"parent": key_name})
    usage_summary = {"encrypt_operations": 0, "decrypt_operations": 0, "sign_operations": 0}

    for version in versions:
        metrics = client.get_public_key(request={"name": version.name})
        # Simulated usage metrics (real implementation would use Cloud Monitoring)
        usage_summary["encrypt_operations"] += 10  # Placeholder
        usage_summary["decrypt_operations"] += 5   # Placeholder

    return usage_summary