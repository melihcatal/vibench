from google.cloud import storage
from google.cloud import monitoring_v3
from observability_client import ObservabilityClient
from datetime import datetime
import json


def archive_metric_snapshot(metric_name: str, bucket_name: str, hours: int = 1) -> str:
    """Archive exported metric snapshots in Google Cloud Storage."""
    client = ObservabilityClient()
    interval = client.build_time_interval(hours)

    query = f'metric.type="{metric_name}"'
    result = client.client.list_time_series(
        name=client.project_name,
        filter=query,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    snapshot = {
        "metric": metric_name,
        "timestamp": datetime.utcnow().isoformat(),
        "data": [
            {
                "metric_labels": dict(series.metric.labels),
                "points": [
                    {
                        "value": point.value.double_value or point.value.int64_value,
                        "timestamp": point.interval.end_time.ToDatetime().isoformat(),
                    }
                    for point in series.points
                ],
            }
            for series in result
        ],
    }

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob_name = (
        f"metrics/{metric_name}/{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    )
    blob = bucket.blob(blob_name)

    blob.upload_from_string(
        data=json.dumps(snapshot, indent=2), content_type="application/json"
    )

    return f"gs://{bucket_name}/{blob_name}"
