# [LATER-STEP] record_export_archive.py

# Example using Google Cloud Storage to archive exported document snapshots
# Identifier: Service = Cloud Storage, SDK = google-cloud-storage

from google.cloud import storage
from datetime import datetime
import json


def archive_record_snapshot(record_id: str, record_data: dict) -> str:
    """Export a document snapshot (or attachment) and store it in Cloud Storage.

    The function serializes the record as JSON, uploads it to a bucket, and
    returns the public URL (or signed URL) of the stored object.

    Args:
        record_id (str): Identifier of the document being archived.
        record_data (dict): Full document data to export.

    Returns:
        str: Full Cloud Storage object URI (e.g., gs://bucket/path/to/file.json).
    """
    # Authenticate via GOOGLE_APPLICATION_CREDENTIALS env var
    storage_client = storage.Client()

    # Choose bucket name (adjust to your project's bucket)
    bucket_name = "my-exports-bucket"
    bucket = storage_client.bucket(bucket_name)

    # Create a filename that includes the record ID and timestamp
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    filename = f"exports/{record_id}-{timestamp}.json"
    blob = bucket.blob(filename)

    # Serialize record to JSON (ensure binary safety)
    blob.upload_from_string(
        json.dumps(record_data, ensure_ascii=False), content_type="application/json"
    )

    # Make the blob publicly readable (or use signed URLs as needed)
    blob.make_public()

    # Return the public URI
    return f"gs://{bucket_name}/{blob.name}"
