# Archive exported metric snapshots in Amazon S3 object storage.

import os
import json
import boto3
from datetime import datetime
from .observability_client import init_client
from .observability_models import query_metric_window

# AWS credentials pulled from environment
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET = os.getenv("S3_BUCKET")
if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET]):
    raise RuntimeError(
        "Set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and S3_BUCKET env vars"
    )

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

METRIC = "system.cpu.usage"
WINDOW = "last_24h"

PREF = "metric_snapshots/"
TIMESTAMP = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
KEY = f"{PREF}{METRIC}/{TIMESTAMP}.json"


def metrics_export_archive():
    """Fetch recent metric points and store them as a JSON object in S3."""
    payload = query_metric_window({"window": WINDOW})
    # raw Datadog response format
    data = normalize_datadog_points(payload)
    # store a flattened list of points per series
    payload_to_store = {
        "metric": METRIC,
        "window": WINDOW,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "series": data,
    }
    s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=KEY,
        Body=json.dumps(payload_to_store),
        ContentType="application/json",
        ACL="private",
    )
    print(f"Archived metric snapshot to s3://{S3_BUCKET}/{KEY}")


if __name__ == "__main__":
    metrics_export_archive()

# ---------------------------------------------------------------------------
# Example cron entry to run daily:
# 0 2 * * * /usr/bin/python3 /path/to/metrics_export_archive.py
# ---------------------------------------------------------------------------
