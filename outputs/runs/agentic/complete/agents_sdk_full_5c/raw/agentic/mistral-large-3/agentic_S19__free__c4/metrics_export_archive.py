import os
from datetime import datetime
from google.cloud import storage
from observability_models import MetricDataPoint
import json


def upload_to_gcs(bucket_name: str, destination_blob_name: str, data: str) -> None:
    """Upload data to Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(data)


def metrics_export_archive(
    metric_data: list[MetricDataPoint], bucket_name: str, metric_name: str
) -> str:
    """Archive exported metric snapshots in Google Cloud Storage."""
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    destination_blob_name = f"metrics/{metric_name}/{timestamp}.json"

    data = json.dumps([point.dict() for point in metric_data])
    upload_to_gcs(bucket_name, destination_blob_name, data)

    return f"gs://{bucket_name}/{destination_blob_name}"