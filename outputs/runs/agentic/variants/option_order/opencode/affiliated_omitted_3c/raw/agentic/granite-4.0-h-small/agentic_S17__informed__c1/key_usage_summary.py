import json
import datetime
from typing import List

from google.cloud import kms_v1

# Google Cloud KMS client (shared)
kms_client = kms_v1.KeyManagementServiceClient()

# Config via env vars (same as other helpers)
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION_ID = os.getenv("KMS_LOCATION", "global")
KEY_RING_ID = os.getenv("KMS_KEY_RING")


def summarize_key_usage(key_id: str) -> List[Dict]:
    """Retrieve recent CryptoKeyVersion usage events for a KMS key.

    Returns a list of dicts with usage summary fields.
    (Real SDK would expose audit logs; here we simulate a structure.)
    """
    key_path = kms_client.crypto_key_path(
        project=PROJECT_ID,
        location=LOCATION_ID,
        key_ring=KEY_RING_ID,
        crypto_key=key_id,
    )
    # Placeholder: fetch audit logs (in real code use kms_client.get_crypto_key_version and audit log APIs)
    # For demonstration we return a fabricated list of events
    return [
        {
            "operation": "encrypt",
            "timestamp": (
                datetime.datetime.utcnow() - datetime.timedelta(minutes=i)
            ).isoformat()
            + "Z",
            "outcome": "success",
            "payload_size_bytes": 1024 * i,
            "key_version": f"{key_id}-v{5 - i}",
        }
        for i in range(5)
    ]
