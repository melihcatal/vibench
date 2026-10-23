from google.cloud import kms
from security_client import get_kms_client
from datetime import datetime, timezone

def summarize_key_usage(project_id: str, location_id: str, key_ring_id: str, key_id: str) -> dict:
    """Summarizes key usage by listing key versions and their creation times from Google Cloud KMS.

    In a real-world scenario, a more comprehensive summary would involve querying Cloud Logging
    for cryptoKey.encrypt, cryptoKey.decrypt, etc., operations and aggregating metrics.
    This function provides a basic summary based on available key metadata.
    """
    client = get_kms_client()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    summary = {
        "key_name": key_name,
        "total_key_versions": 0,
        "key_versions": []
    }

    # List all key versions for the given key
    for version in client.list_crypto_key_versions(parent=key_name):
        summary["total_key_versions"] += 1
        summary["key_versions"].append({
            "version_name": version.name,
            "state": kms.CryptoKeyVersion.CryptoKeyVersionState(version.state).name,
            "create_time": version.create_time.isoformat() if version.create_time else "N/A",
            "algorithm": kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm(version.algorithm).name if version.algorithm else "N/A",
        })

    # Further improvements would involve integrating with Cloud Monitoring for metrics
    # or Cloud Logging for detailed event analysis (e.g., specific encryption/decryption calls).

    return summary

if __name__ == '__main__':
    # Example usage - replace with your actual project, location, key ring, and key IDs
    PROJECT_ID = "your-gcp-project-id"
    LOCATION_ID = "global"  # Or a specific region
    KEY_RING_ID = "your-key-ring-id"
    KEY_ID = "your-symmetric-key-id" # Or any key for which you want usage summary

    try:
        usage_summary = summarize_key_usage(PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID)
        import json
        print(json.dumps(usage_summary, indent=2))
    except Exception as e:
        print(f"Error summarizing key usage: {e}")
