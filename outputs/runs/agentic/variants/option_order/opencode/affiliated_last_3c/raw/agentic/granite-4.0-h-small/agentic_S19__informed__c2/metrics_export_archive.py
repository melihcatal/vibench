# [LATER-STEP] metrics_export_archive.py

# Archive exported metric snapshots in managed object storage (Amazon S3).
# Provider: Amazon S3 (boto3 SDK)

import os
import json
from datetime import datetime
from typing import Dict

import boto3
from boto3.s3.transfer import TransferConfig


def archive_metric_snapshot(
    snapshot_id: str, bucket_name: str, prefix: str = "metrics"
) -> Dict[str, str]:
    """
    Stores a JSON snapshot of exported metrics into an S3 bucket.
    Generates a unique key using the current UTC timestamp.

    Returns a dict with the S3 object key and version ID after upload.
    """
    # Grab credentials from environment (standard AWS vars)
    s3 = boto3.client("s3")
    # Create a machine‑readable payload
    payload = {
        "snapshot_id": snapshot_id,
        "archived_at": datetime.utcnow().isoformat() + "Z",
        "metadata": {
            # Placeholder – in real use you could embed metric metadata here
        },
    }
    key = f"{prefix}/{snapshot_id}_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.json"
    # Upload the JSON payload (pretty‑printed for readability)
    json_str = json.dumps(payload, indent=2)
    transfer_config = TransferConfig(use_threads=True)
    try:
        s3.put_object(
            Bucket=bucket_name, Key=key, Body=json_str, ContentType="application/json"
        )
    except Exception as exc:
        raise RuntimeError(f"Failed to archive metric snapshot to S3: {exc}")
    return {
        "key": key,
        "version_id": s3.head_object(Bucket=bucket_name, Key=key).get("VersionId", ""),
    }
