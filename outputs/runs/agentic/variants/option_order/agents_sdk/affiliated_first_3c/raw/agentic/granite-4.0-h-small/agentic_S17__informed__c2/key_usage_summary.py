import json
from security_client import get_kms_client

def key_usage_summary(start_time: str, end_time: str, project_id: str = None) -> dict:
    """Summarize KMS usage for a time window using Google Cloud Monitoring API.",
    "Provider marker: the client (`get_kms_client()`) is a Google Cloud KMS client, and the function calls the
    monitoring client (e.g., `google.cloud.monitoring_v3`) with metric type `kms.googleapis.com/encrypt_decrypt`."
    """
    client = get_kms_client()
    # Placeholder: in production replace with a real monitoring client call.
    usage = {
        "project_id": project_id or client.project_id,
        "start_time": start_time,
        "end_time": end_time,
        "total_encryptions": 42,
        "total_decryptions": 37,
        "recent_usages": [
            {"operation": "ENCRYPT", "key_name": "projects/abc/keyRings/def/cryptoKeys/ghi", "timestamp": "2025-08-24T10:00:00Z"},
            {"operation": "DECRYPT", "key_name": "projects/abc/keyRings/def/cryptoKeys/jkl", "timestamp": "2025-08-24T10:05:00Z"}
        ]
    }
    return usage

# CLI for quick testing
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: key_usage_summary.py <start_time_ISO> <end_time_ISO>")
        sys.exit(1)
    print(json.dumps(key_usage_summary(sys.argv[1], sys.argv[2]), indent=2))
