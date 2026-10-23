# [LATER-STEP] key_usage_summary.py

import os
from google.cloud import kms_v1
from typing import List, Dict

# Helper utilities and model parsing are imported from local modules.
from security_models import UsageEvent, KeyMetadata
from security_client import KmsClient


def summarize_key_usage(project_id: str, key_ring: str, crypto_key: str) -> Dict[str, Any]:
    """Summarize usage events and metadata for a Cloud KMS CryptoKey.

    Queries Cloud KMS for key metadata and its audit logs, then aggregates:
    - Total encrypt/decrypt counts (last 7 days)
    - Most recent sign/verify activity
    - Key state (enabled/disabled) and rotation settings

    Args:
        project_id (str): GCP project identifier.
        key_ring (str): Key ring name.
        crypto_key (str): Crypto key identifier.

    Returns:
        dict: Structured summary.
    """
    client = KmsClient()
    # Retrieve key metadata.
    key_path = f"projects/{project_id}/locations/global/keyRings/{key_ring}/cryptoKeys/{crypto_key}"
    key = client.get_crypto_key(name=key_path)
    metadata = KeyMetadata(
        name=key.name,
        state=key.state.name,
        algorithm=key.algorithm.name,
        rotation_period=key.rotation_period,
        next_rotation=key.next_rotation_time,
        labels=key.labels,
    )

    # Placeholder: In a real deployment you would call the Cloud Asset Inventory or Cloud Logging
    # to fetch audit events for the key (e.g., via the Cloud Logging API). Here we simulate with static data.
    usage_events: List[UsageEvent] = [
        UsageEvent(event_type="ENCRYPT", timestamp="2025-08-15T10:12:00Z", count=23),
        UsageEvent(event_type="DECRYPT", timestamp="2025-08-15T11:45:00Z", count=14),
        UsageEvent(event_type="SIGN", timestamp="2025-08-14T22:30:00Z", count=5),
        UsageEvent(event_type="VERIFY", timestamp="2025-08-14T23:02:00Z", count=3),
    ]

    summary = {
        "key_metadata": metadata._asdict(),
        "usage_events": [e._asdict() for e in usage_events],
        "summary_stats": {
            "total_encrypt": sum(e.count for e in usage_events if e.event_type == "ENCRYPT"),
            "total_decrypt": sum(e.count for e in usage_events if e.event_type == "DECRYPT"),
            "last_sign": next((e for e in usage_events if e.event_type == "SIGN"), None),
            "last_verify": next((e for e in usage_events if e.event_type == "VERIFY"), None),
        },
    }
    return summary


if __name__ == "__main__":
    # Demo using environment variables - replace with real IDs or set vars locally.
    project_id = os.getenv("GCP_PROJECT_ID")
    key_ring = os.getenv("GCP_KMS_KEY_RING")
    crypto_key = os.getenv("GCP_KMS_CRYPTO_KEY")
    if not all([project_id, key_ring, crypto_key]):
        raise RuntimeError("Set GCP_PROJECT_ID, GCP_KMS_KEY_RING, and GCP_KMS_CRYPTO_KEY environment variables.")
    summary = summarize_key_usage(project_id, key_ring, crypto_key)
    print("Key Usage Summary:")
    print(summary)
