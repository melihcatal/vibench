import os
from google.cloud import kms_v1
from functools import lru_cache


class KmsClientManager:
    """A manager for handling KMS clients."""

    @staticmethod
    @lru_cache(maxsize=1)
    def get_kms_client() -> kms_v1.KeyManagementServiceClient:
        """
        Initializes and returns a Google Cloud KMS client.
        Authentication is handled automatically via Google Cloud SDK credentials.
        """
        # The client uses GOOGLE_APPLICATION_CREDENTIALS environment variable
        # for authentication by default.
        return kms_v1.KeyManagementServiceClient()

    @staticmethod
    def build_key_name(
        project_id: str, location: str, key_ring: str, key_id: str
    ) -> str:
        """Constructs the full key resource name for Google Cloud KMS."""
        return (
            f"projects/{project_id}/locations/{location}/"
            f"keyRings/{key_ring}/keys/{key_id}"
        )

    @staticmethod
    def build_key_version_name(
        project_id: str, location: str, key_ring: str, key_id: str, version: str
    ) -> str:
        """Constructs the full key version resource name for Google Cloud KMS."""
        return (
            f"projects/{project_id}/locations/{location}/"
            f"keyRings/{key_ring}/keys/{key_id}/cryptoKeyVersions/{version}"
        )


def get_gcp_kms_client():
    """Provides a singleton instance of the KMS client."""
    return KmsClientManager.get_kms_client()


def get_key_name_from_env():
    """Retrieves key details from environment variables to construct a key name."""
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_KMS_LOCATION", "global")
    key_ring = os.environ.get("GCP_KMS_KEY_RING")
    key_id = os.environ.get("GCP_KMS_KEY_ID")

    if not all([project_id, location, key_ring, key_id]):
        raise ValueError("Missing GCP KMS environment variables for key configuration.")

    return KmsClientManager.build_key_name(project_id, location, key_ring, key_id)


def get_key_version_name_from_env():
    """Retrieves key version details from environment variables."""
    key_name_parts = get_key_name_from_env().split("/")
    key_version = os.environ.get("GCP_KMS_KEY_VERSION", "1")
    return f"{'/'.join(key_name_parts)}/cryptoKeyVersions/{key_version}"
