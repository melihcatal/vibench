import os
from google.cloud import storage


def archive_document_snapshot(
    document_id: str, content: str, content_type: str = "application/json"
):
    bucket_name = os.environ.get("GCS_BUCKET_NAME")
    if not bucket_name:
        return {
            "status": "error",
            "message": "GCS_BUCKET_NAME not found in environment variables.",
        }

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(f"archive/{document_id}.json")
    blob.upload_from_string(content, content_type=content_type)
    return {
        "status": "success",
        "archive_uri": f"gs://{bucket_name}/archive/{document_id}.json",
    }
