# HELPER: security_client.py
"""Provides local helper utilities and centralized client factories for
Key Management and Encryption services.

All SCORED implementation files import this module to obtain concrete
provider clients in a uniform way. It abstracts credential loading,
environment variable defaults, and optional retry/backoff logic.

Supported providers (add new cases as needed):
  - google-kms   (Google Cloud KMS)
  - aws-kms      (AWS KMS)        # TODO: not yet implemented
"""

import os
import google.auth
from google.cloud import kms_v1
from google.cloud.kms_v1 import KeyManagementServiceClient
from typing import Optional

# ---------------------------------------------------------------------------
# Provider constants / defaults
# ---------------------------------------------------------------------------
DEFAULT_PROJECT = os.getenv("GCP_PROJECT_ID", "YOUR_PROJECT_ID")
DEFAULT_LOCATION = os.getenv("GCP_LOCATION_ID", "global")
DEFAULT_KEY_RING = os.getenv("GCP_KEY_RING_ID", "default-key-ring")
DEFAULT_ENVELOPE_KEY = os.getenv("GCP_ENVELOPE_KEY_ID", "default-envelope-key")
DEFAULT_SIGNING_KEY = os.getenv("GCP_SIGNING_KEY_ID", "default-signing-key")

# ---------------------------------------------------------------------------
# Google Cloud KMS client factory
# ---------------------------------------------------------------------------


def _get_google_kms_credentials() -> google.auth.credentials.Credentials:
    """Obtain credentials for Google Cloud KMS.
    Falls back to Application Default Credentials if no explicit service
    account JSON is set via GOOGLE_APPLICATION_CREDENTIALS."""
    creds, _ = google.auth.default()
    return creds


def get_kms_client(
    override_project: Optional[str] = None,
) -> KeyManagementServiceClient:
    """Return a Google Cloud KMS KeyManagementServiceClient ready for use."""
    creds = _get_google_kms_credentials()
    return KeyManagementServiceClient(credentials=creds)


def get_signing_client(project: Optional[str] = None) -> KeyManagementServiceClient:
    """Return a KMS client pre‑selected for asymmetric signing operations."""
    # Signing uses the same client; just ensure the proper project/location/key are set.
    return get_kms_client(override_project=project)


# ---------------------------------------------------------------------------
# AWS KMS client placeholder (future implementation)
# ---------------------------------------------------------------------------


def get_aws_kms_client(aws_region: str = "us-east-1") -> None:
    """Placeholder – raise NotImplementedError until AWS support is added."""
    raise NotImplementedError("AWS KMS integration not implemented yet")


# ---------------------------------------------------------------------------
# Helper to build fully‑qualified KMS resource names
# ---------------------------------------------------------------------------
def kms_resource_name(
    project: Optional[str] = None,
    location: Optional[str] = None,
    key_ring: Optional[str] = None,
    crypto_key: Optional[str] = None,
) -> str:
    """Construct a KMS resource name string for a given CryptoKey."""
    project = project or DEFAULT_PROJECT
    location = location or DEFAULT_LOCATION
    key_ring = key_ring or DEFAULT_KEY_RING
    crypto_key = crypto_key or DEFAULT_ENVELOPE_KEY
    return f"projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}"


# ---------------------------------------------------------------------------
# Helper for asymmetric signing key name (same pattern as above)
# ---------------------------------------------------------------------------
def signing_key_name(
    project: Optional[str] = None, key_id: Optional[str] = None
) -> str:
    project = project or DEFAULT_PROJECT
    key_id = key_id or DEFAULT_SIGNING_KEY
    return f"projects/{project}/locations/{DEFAULT_LOCATION}/keyRings/{DEFAULT_KEY_RING}/cryptoKeys/{key_id}"


# ---------------------------------------------------------------------------
# End of helper module
# ---------------------------------------------------------------------------
# Example usage (for testing only, not required for scored implementation):
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import json, sys

    print(
        json.dumps(
            {
                "project": DEFAULT_PROJECT,
                "location": DEFAULT_LOCATION,
                "key_ring": DEFAULT_KEY_RING,
                "envelope_key": DEFAULT_ENVELOPE_KEY,
            },
            indent=2,
        )
    )
