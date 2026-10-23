import os
from google.cloud import kms
from google.cloud.kms_v1.types import KeyManagementService
from security_client import get_kms_client, KMSConfig
from datetime import datetime, timedelta

def summarize_key_usage(days: int = 7) -> dict:
    client = get_kms_client()
    key_name = client.crypto_key_path(
        KMSConfig.project_id, KMSConfig.location_id, KMSConfig.key_ring_id, KMSConfig.key_id
    )

    now = datetime.utcnow()
    start_time = now - timedelta(days=days)

    # List crypto operations
    operations = []
    for op in client.list_import_jobs(
        request={"parent": key_name.rsplit("/cryptoKeys", 1)[0]}
    ):
        if op.create_time >= start_time:
            operations.append({
                "operation": "import_job",
                "time": op.create_time.isoformat(),
                "state": op.state.name
            })

    for op in client.list_crypto_key_versions(
        request={"parent": key_name}
    ):
        if op.create_time >= start_time:
            operations.append({
                "operation": "key_version",
                "time": op.create_time.isoformat(),
                "state": op.state.name
            })

    return {
        "key_id": KMSConfig.key_id,
        "project_id": KMSConfig.project_id,
        "operations": operations
    }