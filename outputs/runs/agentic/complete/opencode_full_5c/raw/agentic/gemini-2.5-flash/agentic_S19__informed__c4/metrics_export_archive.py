import os
from google.cloud import storage
from observability_models import MetricExportArchiveRequest


def archive_metric_snapshot(request: MetricExportArchiveRequest) -> str:
    client = storage.Client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.destination_blob_name)

    blob.upload_from_string(request.data)

    return f"gs://{request.bucket_name}/{request.destination_blob_name}"
