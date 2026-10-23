# Archive exported metric snapshots in managed object storage

import os
import json
import hashlib
from datetime import datetime, timezone
from observability_models import MetricQueryRequest, MetricResult, normalize_metric_response
from observability_client import ObservabilityClient

# -------------------------------------------------
# Configuration (adjust if you use a different storage provider)
# -------------------------------------------------
STORAGE_PROVIDER = "Amazon S3"  # could be Backblaze B2, Azure Blob, etc.
# AWS credentials are expected as environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_BUCKET_NAME = os.getenv("AWS_S3_BUCKET", "metrics-archive")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
# -------------------------------------------------


def archive_metric_snapshot(
    provider: str,
    metric_name: str,
    start_relative: str = "-24h",
    end_relative: str = "now",
    granularity_seconds: int = 60,
    region: str = "us-east-1"
) -> str:
    """
    Retrieve a metric snapshot, serialize it to JSON, and store it in the configured object storage.
    Returns the generated object key (e.g., path) where the snapshot was saved.

    :param provider: monitored service identifier (Datadog, Azure Monitor, CloudWatch, etc.)
    :param metric_name: fully qualified metric identifier
    :param start_relative: relative start token (e.g., "-24h")
    :param end_relative: relative end token (e.g., "now")
    :param granularity_seconds: bucket size for aggregation (default 1‑min)
    :param region: optional region/tenant identifier
    :return: storage key/path of the archived file
    """
    start_dt, end_dt = _parse_relative_times(start_relative, end_relative)

    request = MetricQueryRequest(metric_name, start_dt.isoformat(), end_dt.isoformat(), limit=2000)
    client = ObservabilityClient(provider, region=region)
    endpoint = "/query?from={}&to={}&limit=2000&granularity={}".format(
        int(start_dt.timestamp()), int(end_dt.timestamp()), granularity_seconds
    )
    raw = client.request("GET", endpoint, params={"metric": metric_name})
    resp = normalize_metric_response(provider, raw)
    snapshot = resp.data  # list of {timestamp, value}

    # ----- Serialize snapshot -------------------------------------------------
    payload = {
        "provider": provider,
        "metric": metric_name,
        "region": region,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "snapshot": snapshot,
        "metadata": resp.metadata
    }
    json_body = json.dumps(payload, indent=2, sort_keys=True)

    # ----- Compute deterministic key (hash of content) ------------------------
    digest = hashlib.sha256(json_body.encode('utf-8')).hexdigest()
    key = f"snapshots/{metric_name}/{digest[:12]}.json"

    # ----- Store in object storage --------------------------------------------
    if STORAGE_PROVIDER == "Amazon S3":
        # Use boto3 S3 client
        import boto3, botocore
        s3 = boto3.client(
            "s3",
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        s3.put_object(Bucket=AWS_BUCKET_NAME, Key=key, Body=json_body.encode('utf-8'))
    elif STORAGE_PROVIDER == "Backblaze B2":
        # Placeholder for B2 SDK usage
        raise NotImplementedError("Backblaze B2 is not implemented in this stub")
    elif STORAGE_PROVIDER == "Google Cloud Storage":
        # Placeholder for GCS client usage
        raise NotImplementedError("GCS is not implemented in this stub")
    elif STORAGE_PROVIDER == "Azure Blob Storage":
        # Placeholder for Azure Blob SDK usage
        raise NotImplementedError("Azure Blob is not implemented in this stub")
    elif STORAGE_PROVIDER == "IBM Cloud Object Storage":
        # Placeholder for IBM COS SDK usage
        raise NotImplementedError("IBM COS is not implemented in this stub")
    else:
        raise ValueError(f"Unsupported storage provider: {STORAGE_PROVIDER}

    return key


def _parse_relative_times(start_expr: str, end_expr: str) -> (datetime.datetime, datetime.datetime):
    """
    Token parser reused from earlier modules. Returns naive UTC datetimes.
    """
    now = datetime.datetime.utcnow()
    if start_expr.startswith("-"):
        amount, unit = start_expr[1:].split("m") if start_expr.endswith("m") else start_expr[1:].split("h")
        amount = int(amount)
        dt = now - (datetime.timedelta(minutes=amount) if unit.endswith("m") else datetime.timedelta(hours=amount))
    else:
        dt = datetime.datetime.fromisoformat(start_expr.replace("Z", "+00:00"))
    start_dt = dt

    if end_expr.startswith("-"):
        amount, unit = end_expr[1:].split("m") if end_expr.endswith("m") else end_expr[1:].split("h")
        amount = int(amount)
        dt = now - (datetime.timedelta(minutes=amount) if unit.endswith("m") else datetime.timedelta(hours=amount))
    else:
        dt = datetime.datetime.fromisoformat(end_expr.replace("Z", "+00:00"))
    end_dt = dt
    return start_dt, end_dt

# Example usage (remove or move to a test file if desired)
if __name__ == "__main__":
    key = archive_metric_snapshot(
        provider="Datadog",
        metric_name="system.cpu.user",
        start_relative="-1h",
        end_relative="now"
    )
    print(f"Metric snapshot archived under S3 key: {key}")
