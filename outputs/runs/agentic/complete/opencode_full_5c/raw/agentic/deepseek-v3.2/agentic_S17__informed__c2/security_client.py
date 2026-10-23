import os
from typing import Optional
from google.cloud import kms


def get_kms_client() -> kms.KeyManagementServiceClient:
    """
    Create and return a Google Cloud KMS client.
    Uses GOOGLE_APPLICATION_CREDENTIALS environment variable for authentication.
    """
    # Google Cloud KMS client will automatically use GOOGLE_APPLICATION_CREDENTIALS
    # or default application credentials
    return kms.KeyManagementServiceClient()


def get_kms_key_path(
    project_id: str, location: str, key_ring: str, key_name: str
) -> str:
    """
    Construct a KMS key resource path.
    Format: projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{key}
    """
    return f"projects/{project_id}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{key_name}"


def get_kms_key_version_path(
    project_id: str, location: str, key_ring: str, key_name: str, version: str
) -> str:
    """
    Construct a KMS key version resource path.
    Format: projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{key}/cryptoKeyVersions/{version}
    """
    return f"projects/{project_id}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{key_name}/cryptoKeyVersions/{version}"


def load_config() -> dict:
    """
    Load configuration from environment variables.
    """
    config = {
        "google_cloud_project": os.getenv("GOOGLE_CLOUD_PROJECT"),
        "kms_location": os.getenv("KMS_LOCATION", "global"),
        "kms_key_ring": os.getenv("KMS_KEY_RING", "default"),
        "default_key_name": os.getenv("DEFAULT_KMS_KEY", "encryption-key"),
    }

    # Validate required configuration
    if not config["google_cloud_project"]:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    return config


def get_default_key_path() -> str:
    """
    Get the default KMS key path using configuration.
    """
    config = load_config()
    return get_kms_key_path(
        project_id=config["google_cloud_project"],
        location=config["kms_location"],
        key_ring=config["kms_key_ring"],
        key_name=config["default_key_name"],
    )
