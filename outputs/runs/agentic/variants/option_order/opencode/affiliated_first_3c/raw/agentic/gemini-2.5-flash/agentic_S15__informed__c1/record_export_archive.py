import os
from google.cloud import storage
from typing import Dict, Any


def archive_document_snapshot(
    document_id: str,
    snapshot_data: Dict[str, Any],
    bucket_name: str,
    destination_blob_name: str,
) -> str:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Upload the document snapshot as a JSON string
    blob.upload_from_string(data=str(snapshot_data), content_type="application/json")

    return f"gs://{bucket_name}/{destination_blob_name}"
