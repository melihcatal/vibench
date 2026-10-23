import os
from google.cloud import kms_v1


def get_kms_client():
    """Returns a Google Cloud KMS client."""
    return kms_v1.KeyManagementServiceClient()


def get_key_path(
    project_id: str, location_id: str, key_ring_id: str, key_id: str
) -> str:
    """Constructs the fully qualified key path for Google Cloud KMS.

    Args:
        project_id: Your Google Cloud project ID.
        location_id: The GCP location of the key ring (e.g., 'global', 'us-central1').
        key_ring_id: The ID of the key ring.
        key_id: The ID of the key.

    Returns:
        The fully qualified key path.
    """
    return get_kms_client().crypto_key_path(
        project_id, location_id, key_ring_id, key_id
    )


def get_key_version_path(
    project_id: str,
    location_id: str,
    key_ring_id: str,
    key_id: str,
    key_version_id: str,
) -> str:
    """Constructs the fully qualified key version path for Google Cloud KMS.

    Args:
        project_id: Your Google Cloud project ID.
        location_id: The GCP location of the key ring (e.g., 'global', 'us-central1').
        key_ring_id: The ID of the key ring.
        key_id: The ID of the key.
        key_version_id: The ID of the key version.

    Returns:
        The fully qualified key version path.
    """
    return get_kms_client().crypto_key_version_path(
        project_id, location_id, key_ring_id, key_id, key_version_id
    )
