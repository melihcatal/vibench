import json
from datetime import datetime
from google.cloud import kms_v1
from security_client import KMSClient

def key_usage_summary(key_name: str) -> str:
    """Produce a summary of key usage metrics and recent crypto events.

    The summary includes:
    - Number of encrypt calls in the last 24h
    - Number of decrypt calls in the last 24h
    - Last encrypt timestamp
    - Last decrypt timestamp
    
    For Cloud KMS this information is derived from audit logs (Cloud Logging) and the
    KMS key metadata's usage metrics. This example reads the audit logs via a simplified
    helper that assumes audit logs are exported to a BigQuery table `kms_audit.events`.
    
    Args:
        key_name (str): Full Cloud KMS key name (projects/*/locations/*/keyRings/*/cryptoKeys/*).
    
    Returns:
        str: JSON string containing the usage summary.
    """
    client = KMSClient()
    project_id = client.project_id
    location = client.location
    crypto_key_id = key_name.split('/')[-1]
    
    # ---- Query audit events from BigQuery (pseudo‑code) ----
    # In a production deployment you would query a table that receives cloud audit logs for
    # the key. Here we simulate with dummy data.
    summary = {
        'key_name': key_name,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'usage_last_24h': {
            'encrypt_calls': 0,   # placeholder
            'decrypt_calls': 0,   # placeholder
        },
        'last_events': {
            'encrypt': None,
            'decrypt': None
        }
    }
    return json.dumps(summary, indent=2)
