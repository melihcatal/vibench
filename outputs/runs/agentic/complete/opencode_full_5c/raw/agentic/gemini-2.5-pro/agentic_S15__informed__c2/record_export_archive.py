import os
import json
from google.cloud import storage
from database_models import Document


def archive_document(record: Document, bucket_name: str) -> str:
    """
    Archives a document snapshot to Google Cloud Storage.

    Args:
        record: The document record to archive.
        bucket_name: The name of the GCS bucket.

    Returns:
        The public URL of the archived object.
    """
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        document_id = record.get("document_id", "unknown_document")
        version = record.get("version", "latest")
        blob_name = f"archive/{document_id}/v{version}.json"

        blob = bucket.blob(blob_name)

        # Serialize the document to a JSON string
        document_json = json.dumps(record, indent=2)

        blob.upload_from_string(document_json, content_type="application/json")

        return blob.public_url
    except Exception as e:
        print(f"An error occurred during archival: {e}")
        raise
