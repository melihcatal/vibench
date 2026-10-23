import os
from google.cloud import kms
from google.cloud import logging
from security_client import get_kms_client
from typing import List, Dict

def summarize_key_usage() -> List[Dict]:
    client = get_kms_client()
    logging_client = logging.Client()
    key_name = client.crypto_key_path(
        os.getenv("GCP_PROJECT_ID"),
        os.getenv("GCP_LOCATION_ID"),
        os.getenv("GCP_KEY_RING_ID"),
        os.getenv("GCP_CRYPTO_KEY_ID")
    )

    # Fetch KMS audit logs
    filter_str = (
        f'resource.name="{key_name}" '
        'logName="projects/{}/logs/cloudkms.googleapis.com%2Factivity"'
    ).format(os.getenv("GCP_PROJECT_ID"))

    entries = logging_client.list_entries(filter_=filter_str, max_results=100)
    summary = []

    for entry in entries:
        summary.append({
            "timestamp": entry.timestamp.isoformat(),
            "method": entry.payload.get("methodName"),
            "principal_email": entry.payload.get("authenticationInfo", {}).get("principalEmail"),
            "resource_name": entry.resource.get("labels", {}).get("crypto_key_id")
        })

    return summary