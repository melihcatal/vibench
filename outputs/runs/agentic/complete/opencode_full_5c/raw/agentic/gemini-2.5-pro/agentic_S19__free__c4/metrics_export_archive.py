import json
from google.cloud import storage
from observability_models import ArchiveRequest


def archive_metrics_snapshot(request: ArchiveRequest):
    """
    Archives exported metric snapshots in Google Cloud Storage.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)

    data_str = json.dumps(request.data, indent=2)

    blob.upload_from_string(data_str, content_type="application/json")

    return {
        "bucket": request.bucket_name,
        "object_name": request.object_name,
        "status": "archived",
    }
