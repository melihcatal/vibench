import os
import json
from observability_client import ObservabilityClient
from observability_models import MetricSnapshot
from google.cloud import storage


def metrics_export_archive(
    project_id: str,
    bucket_name: str,
    file_name: str,
    metric_snapshot: MetricSnapshot,
) -> str:
    client = ObservabilityClient(project_id).get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Convert MetricSnapshot dataclass to a dictionary, then to JSON string
    # This assumes MetricSnapshot and its nested dataclasses are serializable
    metric_snapshot_dict = metric_snapshot.__dict__
    # Further serialize nested dataclasses if any
    for key, value in metric_snapshot_dict.items():
        if isinstance(value, list):
            metric_snapshot_dict[key] = [
                (item.__dict__ if hasattr(item, "__dict__") else item) for item in value
            ]
        elif hasattr(value, "__dict__"):
            metric_snapshot_dict[key] = value.__dict__

    content = json.dumps(metric_snapshot_dict, indent=2)

    blob.upload_from_string(content, content_type="application/json")

    return f"gs://{bucket_name}/{file_name}"
