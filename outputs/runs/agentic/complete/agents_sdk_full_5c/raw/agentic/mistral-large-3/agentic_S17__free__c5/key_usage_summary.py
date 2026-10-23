import os
from google.cloud import kms
from google.cloud.kms_v1.types import KeyOperationAttestation
from security_client import get_kms_client
from typing import List, Dict

def summarize_key_usage(project_id: str, location_id: str, key_ring_id: str, key_id: str) -> Dict:
    client = get_kms_client()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Fetch key metadata
    key = client.get_crypto_key(request={"name": key_name})

    # Fetch key version usage (simplified example)
    versions = list(client.list_crypto_key_versions(request={"parent": key_name}))

    usage_summary = {
        "key_id": key_name,
        "purpose": key.purpose.name,
        "algorithm": key.version_template.algorithm.name,
        "versions": len(versions),
        "provider": "google-cloud-kms",
        "model": f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{key_id}"
    }

    return usage_summary