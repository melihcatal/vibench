import os
import json
from collections import defaultdict
from security_client import KmsClient
from security_models import DecryptRequest, EncryptRequest

# Placeholder constants for illustration
KEY_ID = "alias/MyKMSEncryptionKey"

# Simulated event logs (in real use, load from CloudWatch Logs, DynamoDB, etc.)
__FAKE_LOGS__ = [
    {"event": "ENCRYPT", "payload_id": "p1", "timestamp": "2025-08-15T10:01:00Z"},
    {"event": "DECRYPT", "payload_id": "p1", "timestamp": "2025-08-15T10:02:00Z"},
    {"event": "ENCRYPT", "payload_id": "p2", "timestamp": "2025-08-15T10:03:00Z"},
    {"event": "ENCRYPT", "payload_id": "p1", "timestamp": "2025-08-15T10:04:00Z"},
    {"event": "DECRYPT", "payload_id": "p3", "timestamp": "2025-08-15T10:05:00Z"},
]


def _process_log_entry(entry: Dict) -> Dict:
    """Normalises a log entry to a common schema used for summary."""
    ev_type = entry["event"].upper()
    entry_norm = {
        "type": ev_type,
        "payload": entry["payload_id"],
        "time": entry["timestamp"]
    }
    return entry_norm


def summarize_key_usage(key: str = KEY_ID) -> Dict:
    """Aggregates counts of ENCRYPT and DECRYPT events for a given KMS key."""
    kms = KmsClient()  # client initialised but not used for real API calls in this stub
    usage = defaultdict(int)
    for raw in __FAKE_LOGS__:
        norm = _process_log_entry(raw)
        if norm["type"] in ("ENCRYPT", "DECRYPT"):
            usage[norm["type"]] += 1
    return {
        "key_id": key,
        "total_events": sum(usage.values()),
        "encrypt_count": usage["ENCRYPT"],
        "decrypt_count": usage["DECRYPT"],
        "last_event": {
            "type": max(__FAKE_LOGS__, key=lambda e: e["timestamp"]).get("event", "UNKNOWN")
        }
    }

if __name__ == "__main__":
    print(json.dumps(summarize_key_usage(), indent=2))
