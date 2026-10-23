# metrics_export_archive.py

import json
from typing import Any, Dict, List

from observability_client import get_metrics_client

# ---------------------------------------------------------------------------
# Configuration (choose ONE concrete provider)
# ---------------------------------------------------------------------------
# Example: IBM Cloud Monitoring
IBM_MONITORING_INSTANCE_ID = "YOUR_MONITORING_INSTANCE_ID"
IBM_CLOUD_API_KEY = "YOUR_IBM_CLOUD_API_KEY"

# Example: Amazon CloudWatch Metrics (uncomment if using AWS)
# AWS_ACCESS_KEY_ID = "YOUR_AWS_ACCESS_KEY_ID"
# AWS_SECRET_ACCESS_KEY = "YOUR_AWS_SECRET_ACCESS_KEY"

# ---------------------------------------------------------------------------
# Helper: export a snapshot of recent metric data to a normalized format
# ---------------------------------------------------------------------------


def export_snapshot(
    metric_name: str, start: int, end: int, filters: List[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """Fetch raw metric datapoints and convert to a consistent JSON‑serializable schema.
    Returns a list of dictionaries, each representing a single datapoint.
    """
    client = get_metrics_client()
    raw = client.query(
        payload={"metric": metric_name, "start": start, "end": end, "filters": filters}
    )
    # Normalization step (same as used in other modules)
    if "datapoints" in raw:
        return [
            {
                "timestamp": dp.get("timestamp"),
                "value": dp.get("value"),
                "annotations": dp.get("annotations", []),
            }
            for dp in raw.get("datapoints", [])
        ]
    return []


# ---------------------------------------------------------------------------
# Archive upload using managed object storage (IBM COS example)
# ---------------------------------------------------------------------------


def archive_to_storage(
    bucket_name: str, object_key: str, data: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Upload the exported snapshot to managed object storage.
    Returns the storage service response.
    """
    client = get_metrics_client()
    # The client abstraction provides a generic upload_to_cos method (or similar)
    return client.upload_to_cos(
        bucket=bucket_name, key=object_key, body=json.dumps(data)
    )


# ---------------------------------------------------------------------------
# Core orchestration: export then archive
# ---------------------------------------------------------------------------


def export_and_archive(
    metric_name: str,
    start: int,
    end: int,
    filters: List[Dict[str, Any]] = None,
    bucket: str = "metrics-archive",
    prefix: str = "snapshots",
) -> Dict[str, Any]:
    snapshot = export_snapshot(metric_name, start, end, filters)
    object_key = f"{prefix}/{metric_name}/{start}-{end}.json"
    result = archive_to_storage(bucket, object_key, snapshot)
    return {
        "metric": metric_name,
        "start": start,
        "end": end,
        "archived": True,
        "response": result,
    }


# ---------------------------------------------------------------------------
# Example usage (for local testing only)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import time

    now = int(time.time())
    five_min_ago = now - 300
    filters = [{"resource_id": "i-0abcd1234"}]
    result = export_and_archive(
        "memory.usage", start=five_min_ago, end=now, filters=filters
    )
    print(json.dumps(result, indent=2))
