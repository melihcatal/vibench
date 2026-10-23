# [HELPER] security_client.py
# Local helper utilities for constructing Key Management & Encryption clients
import os
import google.auth
from google.cloud import kms_v1


def kms_client_from_config() -> kms_v1.KeyManagementServiceClient:
    """Creates a configured KMS client using credentials from environment variables.

    Expects the following env vars:
        - GOOGLE_APPLICATION_CREDENTIALS: path to a service account JSON
        - KMS_PROJECT_ID
        - KMS_LOCATION_ID
    Returns a ready-to-use kms_v1.KeyManagementServiceClient.
    """
    creds, _ = google.auth.default()  # picks up service account or ADC
    client = kms_v1.KeyManagementServiceClient(credentials=creds)
    return client


def kms_key_name(
    project_id: str, location_id: str, key_ring_id: str, crypto_key_id: str
) -> str:
    """Returns the fully qualified KMS key name string.

    Example: projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}
    """
    return f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}"


# Example usage (can be removed in production)
if __name__ == "__main__":
    client = kms_client_from_config()
    print("KMS client initialized")
    key = kms_key_name(
        os.getenv("KMS_PROJECT_ID"),
        os.getenv("KMS_LOCATION_ID"),
        os.getenv("KMS_KEY_RING_ID"),
        os.getenv("KMS_CRYPTO_KEY_ID"),
    )
    print("Key name:", key)
