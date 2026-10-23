# metrics_export_archive.py
# LATER-STEP: Archive exported metric snapshots in managed object storage

import os
from datetime import datetime
from observability_client import ObservabilityClient
from observability_models import ExportSnapshotRequest, ExportSnapshotResponse


def archive_metric_snapshot(
    metric: str,
    start_time: str = None,
    end_time: str = None,
    window: str = "P1H",
    bucket_path: str = "metric-snapshots",
) -> str:
    """Export a metric snapshot and store it in managed object storage.

    Returns a storage reference (e.g., a URL or object key) that can be
    used to retrieve the archived snapshot later.

    Args:
        metric: Metric name (e.g., "cpu.usage").
        start_time: ISO‑8601 start timestamp (optional).
        end_time: ISO‑8601 end timestamp (optional).
        window: Relative window (e.g., "P1H").
        bucket_path: Logical path inside the bucket where snapshots are stored.

    Returns:
        A string reference to the stored snapshot.
    """
    client = ObservabilityClient()

    # 1) Export the snapshot (provider‑specific endpoint)
    payload = ExportSnapshotRequest(
        metric=metric,
        start_time=start_time,
        end_time=end_time,
        window=window,
    )
    result = client.request("POST", "/export/snapshot", json=payload.to_dict())
    # Example response: {"ref": "2024-07-15T12-00-00_cpu.usage.parquet"}
    raw_ref = result.get("ref")
    if not raw_ref:
        raise RuntimeError("Export service did not return a storage reference")

    # 2) Determine storage location; here we construct a path using the current date
    #    and set the bucket name based on the configured provider (placeholder)
    provider = os.getenv("MONITORING_PROVIDER", "Datadog")
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    final_key = f"{bucket_path}/{provider}_{metric}_{timestamp}.parquet"
    # For a real integration replace this stub with the SDK call to upload the file
    # to the appropriate bucket (e.g., boto3 S3 put_object, or OSS2 upload).
    # Here we simply return the constructed key as the reference.
    return final_key


# Example CLI usage for local testing
if __name__ == "__main__":
    ref = archive_metric_snapshot(metric="disk.space", window="P2H")
    print("Snapshot archived at:", ref)
