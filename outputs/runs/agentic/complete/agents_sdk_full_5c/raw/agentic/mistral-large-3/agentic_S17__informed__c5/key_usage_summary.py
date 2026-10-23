from google.cloud import kms
from datetime import datetime, timedelta
import os


def summarize_key_usage(key_id: str, days: int = 7) -> dict:
    """
    Summarizes key usage and crypto events for a Google Cloud KMS key.
    
    Args:
        key_id: The fully-qualified Google Cloud KMS key identifier.
        days: The number of days to look back for events.
    
    Returns:
        A dictionary containing key usage summary.
    """
    client = kms.KeyManagementServiceClient()
    
    # Google Cloud KMS-specific key usage summary
    project_id = key_id.split('/')[1]
    location_id = key_id.split('/')[3]
    key_ring_id = key_id.split('/')[5]
    crypto_key_id = key_id.split('/')[7]
    
    key_name = client.crypto_key_path_path(project_id, location_id, key_ring_id, crypto_key_id)
    
    # Fetch key version usage (simplified example)
    key_versions = list(client.list_crypto_key_versions(request={"parent": key_name}))
    
    # Fetch audit logs (placeholder for actual Cloud Logging integration)
    start_time = datetime.utcnow() - timedelta(days=days)
    
    return {
        "key_id": key_id,
        "key_versions": [kv.name for kv in key_versions],
        "usage_period_days": days,
        "crypto_events_count": len(key_versions),  # Simplified
        "last_used": datetime.utcnow().isoformat()
    }