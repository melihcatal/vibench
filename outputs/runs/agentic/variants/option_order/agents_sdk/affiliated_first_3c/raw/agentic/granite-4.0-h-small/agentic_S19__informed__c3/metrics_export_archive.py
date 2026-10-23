# metrics_export_archive.py
# LATER-STEP: Archive exported metric snapshots in managed object storage

import os
import json
import boto3
from typing import List, Dict

# Amazon S3 example – uses boto3 client
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_BUCKET_NAME = os.getenv("AWS_S3_BUCKET")
if not (AWS_ACCESS_KEY and AWS_SECRET_KEY and AWS_BUCKET_NAME):
    raise RuntimeError("Set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY and AWS_S3_BUCKET env vars")

s3_client = boto3.client('s3',
                         aws_access_key_id=AWS_ACCESS_KEY,
                         aws_secret_access_key=AWS_SECRET_KEY)

def archive_metric_snapshot(snapshot_id: str, data: List[Dict[str, Any]],
                            archive_key: str | None = None) -> str:
    """
    Persists a JSON representation of a metric snapshot to S3.
    `snapshot_id` is a unique identifier (e.g., ingestion timestamp).
    If `archive_key` is not supplied, a timestamped key is generated.
    Returns the S3 object key where the data is stored.
    """
    if archive_key is None:
        archive_key = f"metrics/{snapshot_id[:10]}/{snapshot_id}.json"
    s3_client.put_object(
        Bucket=AWS_BUCKET_NAME,
        Key=archive_key,
        Body=json.dumps(data, ensure_ascii=False).encode('utf-8')
    )
    return archive_key

# ---------------------------------------------------------------------------
# Example usage (remove or guard with __main__ when integrating into services)
if __name__ == "__main__":
    # Simulated SAME-SCENARIO result (query_metric_window output structure)
    sample_result = {
        "cost": None,
        "data": [
            {"timestamp": "2025-08-15T12:00:00Z", "value": 12.5},
            {"timestamp": "2025-08-15T12:01:00Z", "value": 13.2},
            {"timestamp": "2025-08-15T12:02:00Z", "value": 11.8}
        ]
    }
    key = archive_metric_snapshot("20250815T120000Z", sample_result['data'])
    print("Archived snapshot stored at S3 key:", key)
