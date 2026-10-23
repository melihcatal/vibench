import os
import json
from observable_client import get_provider_client, normalize_response
from observable_models import QueryMetricWindowRequest

PROVIDER = os.getenv("METRICS_PROVIDER", "datadog")


def archive_metric_snapshot(
    metric_name: str, window: str = "1h", archive_path: str = "metric_snapshots.json"
) -> None:
    """Archive an exported metric snapshot in a local JSON file.

    This demonstrates a later‑step integration that persists raw metric data for
    long‑term storage (e.g., object storage). In a production system you would
    upload the JSON to an object store (S3, GCS, IBM COS) instead of a local file.

    Args:
        metric_name: Name of the metric to export.
        window: Time window for the query (e.g., "1h", "24h").
        archive_path: Local path where the JSON snapshot will be written.
    """
    # Query recent datapoints
    start = os.getenv("METRICS_START", "2024-07-01T12:00:00Z")
    end = os.getenv("METRICS_END", "2024-07-01T13:00:00Z")
    req = QueryMetricWindowRequest(
        metric_name=metric_name, start_time=start, end_time=end, limit=200
    )
    client = get_provider_client(PROVIDER)
    raw = client.metrics.query(
        metric=metric_name,
        start=start,
        end=end,
        query=f"avg:{metric_name} over {window} as_rate",
    )
    normalized = normalize_response(raw, PROVIDER)
    datapoints = normalized.get("data", [])

    # Prepare snapshot payload
    snapshot = {
        "metric": metric_name,
        "window": window,
        "timestamp": os.getenv("SNAPSHOT_TIME", "2024-07-01T13:00:00Z"),
        "datapoints": datapoints,
    }

    # Write to JSON file (in production replace with object storage upload)
    with open(archive_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    print(f"Metric snapshot for {metric_name} archived to {archive_path}")


if __name__ == "__main__":
    archive_metric_snapshot(
        metric_name="system.cpu.user", window="1h", archive_path="cpu_snapshot.json"
    )
