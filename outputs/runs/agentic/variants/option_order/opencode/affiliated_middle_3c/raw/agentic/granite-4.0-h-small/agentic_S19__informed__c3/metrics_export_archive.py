# LATER-STEP

import os
import json
import datetime as dt
import boto3

# Provider selection: Amazon S3 (boto3 SDK) used for storing exported metric snapshots

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET = os.getenv("S3_EXPORT_BUCKET", "my-metrics-archive")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def archive_metric_snapshot(snapshot_id: str, snapshot_content: dict):
    """Save the exported metric snapshot as a JSON file in S3.

    Args:
        snapshot_id (str): Unique identifier for the snapshot (e.g., timestamp).
        snapshot_content (dict): Data payload returned from a metric export request.

    Returns:
        dict: S3 upload response metadata.
    """
    key = f"exports/{snapshot_id}.json"
    # Serialize JSON deterministically
    body = json.dumps(snapshot_content, separators=(",", ":"), sort_keys=True).encode(
        "utf-8"
    )
    response = s3_client.put_object(Bucket=S3_BUCKET, Key=key, Body=body)
    return response


# Example (illustrative):
# data = {'metric':'cpu.usage','values':[...]}
# archive_metric_snapshot('20250808T120000Z', data)
