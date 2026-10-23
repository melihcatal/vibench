# LATER-STEP: key_usage_summary.py
"""Summarize key usage events and crypto operations performed.

This script queries the concrete provider (Google Cloud KMS) and aggregates
statistics such as total number of encrypt/decrypt calls, distinct keys used,
and timestamps of recent activity. The output is a JSON report suitable for
review or archival.

Provider identification: imports from ``security_client`` which wraps the
Google Cloud KMS SDK (`google-cloud-kms`).
"""

import json
import datetime
from google.cloud import kms_v1
from google.cloud.kms_v1 import KeyManagementServiceClient
from typing import List, Dict

from security_client import get_kms_client
from security_models import PROVIDER_WHITELIST, validate_provider

# ---------------------------------------------------------------------------
# Configuration (optional env override)
# ---------------------------------------------------------------------------
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "YOUR_PROJECT_ID")
LOCATION_ID = os.getenv("GCP_LOCATION_ID", "global")
KEY_RING_ID = os.getenv("GCP_KEY_RING_ID", "default-key-ring")


def _gcs_timestamp(ts_micros: int) -> str:
    """Convert KMS timestamp in microseconds to ISO 8601 string."""
    # Convert to seconds with fractions
    dt = datetime.datetime.utcfromtimestamp(ts_micros / 1_000_000)
    return dt.isoformat() + "Z"


def generate_usage_summary() -> Dict[str, any]:
    """Return a dict summarizing usage events for the configured key ring."""
    client = get_kms_client()
    # List CryptoKeys in the ring
    keys = client.list_crypto_keys(
        parent=f"projects/{PROJECT_ID}/locations/{LOCATION_ID}/keyRings/{KEY_RING_ID}"
    )
    key_ids = [k.name.split("/")[-1] for k in keys.crypto_keys]
    report = {
        "project_id": PROJECT_ID,
        "location_id": LOCATION_ID,
        "key_ring_id": KEY_RING_ID,
        "keys_reported": len(key_ids),
        "keys": [],
    }
    for key_id in key_ids:
        # Gather basic activity metrics (simple example)
        # In a real implementation you would query audit logs via Cloud Logging API.
        report["keys"].append(
            {
                "key_id": key_id,
                "encrypt_calls": 0,  # placeholder
                "decrypt_calls": 0,  # placeholder
                "last_used": "N/A",
            }
        )
    return report


# ---------------------------------------------------------------------------
# CLI entry point (optional)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    summary = generate_usage_summary()
    print(json.dumps(summary, indent=2))
