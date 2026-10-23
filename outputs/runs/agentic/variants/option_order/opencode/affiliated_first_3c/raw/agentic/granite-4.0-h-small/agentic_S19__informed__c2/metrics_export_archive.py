import os
from observability_client import ObservabilityClient, MetricResponse
from observability_models import MetricAggregatePayload
import json


def archive_metric_snapshot(
    metric_name, start_time, end_time, storage_path="/tmp/metric_snapshots"
):
    """Archive exported metric snapshots in managed object storage.

    Args:
        metric_name (str): Name of the metric.
        start_time (int): Unix timestamp for start of window (seconds).
        end_time (int): Unix timestamp for end of window (seconds).
        storage_path (str): Local directory where snapshots will be written.

    Returns:
        str: Path of the archived snapshot file.
    """
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)
    snapshot_file = os.path.join(
        storage_path, f"{metric_name}_{start_time}_{end_time}.json"
    )
    client = ObservabilityClient()
    payload = MetricAggregatePayload(metric=metric_name, start=start_time, end=end_time)
    response = client.rest_call(
        method="POST", endpoint="/api/v1/metrics/export", json=payload
    )
    normalized = MetricResponse.from_raw(response)
    if normalized.status != "ok":
        return f"Export failed: {normalized.message}"
    # Write the exported JSON to the local snapshot file
    with open(snapshot_file, "w") as f:
        json.dump(normalized.data, f, indent=2)
    return snapshot_file
