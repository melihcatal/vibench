import os
import json
import tempfile
from datetime import datetime
from typing import Dict, Any
from google.cloud import storage
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2


def export_metrics_to_storage(
    metric_name: str, window_hours: int = 24, bucket_name: str = None
) -> Dict[str, Any]:
    """Archive exported metric snapshots in Google Cloud Storage."""

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")

    if not bucket_name:
        bucket_name = f"{project_id}-metrics-archive"

    # Fetch metrics from Google Cloud Monitoring
    monitoring_client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=window_hours)

    interval = monitoring_v3.TimeInterval()
    interval.end_time = timestamp_pb2.Timestamp(seconds=int(end_time.timestamp()))
    interval.start_time = timestamp_pb2.Timestamp(seconds=int(start_time.timestamp()))

    filter_str = f'metric.type = "{metric_name}"'

    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=filter_str,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    metrics_data = []
    for time_series in monitoring_client.list_time_series(request):
        series_data = {
            "metric_type": time_series.metric.type,
            "resource_type": time_series.resource.type,
            "resource_labels": dict(time_series.resource.labels),
            "metric_labels": dict(time_series.metric.labels),
            "points": [],
        }

        for point in time_series.points:
            value = 0.0
            if point.value.HasField("double_value"):
                value = point.value.double_value
            elif point.value.HasField("int64_value"):
                value = float(point.value.int64_value)

            series_data["points"].append(
                {
                    "timestamp": point.interval.end_time.ToDatetime().isoformat(),
                    "value": value,
                }
            )

        metrics_data.append(series_data)

    # Create archive metadata
    archive_metadata = {
        "export_timestamp": datetime.utcnow().isoformat(),
        "metric_name": metric_name,
        "time_window": {
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
            "hours": window_hours,
        },
        "total_series": len(metrics_data),
        "total_points": sum(len(series["points"]) for series in metrics_data),
        "project_id": project_id,
        "provider": "Google Cloud Monitoring",
    }

    # Prepare archive content
    archive_content = {"metadata": archive_metadata, "metrics": metrics_data}

    # Upload to Google Cloud Storage
    storage_client = storage.Client(project=project_id)

    # Create bucket if it doesn't exist
    try:
        bucket = storage_client.get_bucket(bucket_name)
    except Exception:
        bucket = storage_client.create_bucket(bucket_name, location="us-central1")

    # Generate filename with timestamp
    timestamp_str = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"metrics_export/{metric_name.replace('/', '_')}_{timestamp_str}.json"

    # Create blob and upload
    blob = bucket.blob(filename)

    # Set metadata for the blob
    blob.metadata = {
        "metric_name": metric_name,
        "export_time": archive_metadata["export_timestamp"],
        "time_window_start": start_time.isoformat(),
        "time_window_end": end_time.isoformat(),
    }

    # Upload JSON content
    blob.upload_from_string(
        json.dumps(archive_content, indent=2), content_type="application/json"
    )

    # Make the blob publicly readable (optional, for sharing)
    blob.make_public()

    result = {
        "status": "success",
        "archive_location": f"gs://{bucket_name}/{filename}",
        "public_url": blob.public_url,
        "metadata": archive_metadata,
        "storage_provider": "Google Cloud Storage",
        "bucket": bucket_name,
        "file_size": len(json.dumps(archive_content)),
    }

    return result


def list_metric_exports(bucket_name: str = None) -> Dict[str, Any]:
    """List available metric exports in storage bucket."""

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")

    if not bucket_name:
        bucket_name = f"{project_id}-metrics-archive"

    storage_client = storage.Client(project=project_id)

    try:
        bucket = storage_client.get_bucket(bucket_name)
        blobs = list(bucket.list_blobs(prefix="metrics_export/"))

        exports = []
        for blob in blobs:
            exports.append(
                {
                    "name": blob.name,
                    "size": blob.size,
                    "updated": blob.updated.isoformat(),
                    "url": blob.public_url if blob.public_url else None,
                    "metadata": blob.metadata or {},
                }
            )

        return {
            "bucket": bucket_name,
            "total_exports": len(exports),
            "exports": exports,
            "provider": "Google Cloud Storage",
        }

    except Exception as e:
        return {
            "error": str(e),
            "bucket": bucket_name,
            "total_exports": 0,
            "exports": [],
        }


if __name__ == "__main__":
    # Export CPU utilization metrics
    export_result = export_metrics_to_storage(
        "compute.googleapis.com/instance/cpu/utilization",
        window_hours=6,
        bucket_name="my-metrics-archive-bucket",
    )
    print(f"Export result: {export_result}")

    # List existing exports
    exports_list = list_metric_exports("my-metrics-archive-bucket")
    print(f"Total exports: {exports_list.get('total_exports', 0)}")
