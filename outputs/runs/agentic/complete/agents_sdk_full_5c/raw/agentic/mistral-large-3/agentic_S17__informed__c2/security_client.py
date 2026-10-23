from google.cloud import kms
import os

def get_kms_client() -> kms.KeyManagementServiceClient:
    return kms.KeyManagementServiceClient()

def get_kms_key_name(project_id: str, location_id: str, key_ring_id: str, key_id: str) -> str:
    return f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{key_id}"