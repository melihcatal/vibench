from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any
from google.cloud import storage

@dataclass
class MetricExportArchiveRequest:
    project_id: str
    bucket_name: str
    destination_blob_name: str # e.g., metrics_snapshots/2023/04/snapshot_2023-04-23.json
    data_to_archive: str # The content of the snapshot, e.g., JSON string
    content_type: str = "application/json" # e.g., application/json, text/csv

@dataclass
class MetricExportArchiveResponse:
    bucket_name: str
    blob_name: str
    uri: str
    size_bytes: int
    time_created: datetime

def archive_metric_snapshot(request: MetricExportArchiveRequest) -> MetricExportArchiveResponse:
    storage_client = storage.Client(project=request.project_id)
    bucket = storage_client.bucket(request.bucket_name)
    blob = bucket.blob(request.destination_blob_name)

    blob.upload_from_string(request.data_to_archive, content_type=request.content_type)

    # Refresh the blob's metadata to get updated information like size and creation time
    blob.reload()

    return MetricExportArchiveResponse(
        bucket_name=request.bucket_name,
        blob_name=request.destination_blob_name,
        uri=f"gs://{request.bucket_name}/{request.destination_blob_name}",
        size_bytes=blob.size,
        time_created=blob.time_created
    )
