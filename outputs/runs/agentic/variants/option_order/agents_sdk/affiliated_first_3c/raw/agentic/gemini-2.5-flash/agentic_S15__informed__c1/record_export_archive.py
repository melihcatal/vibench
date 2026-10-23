import os
from google.cloud import storage
import json

def record_export_archive(document_records: list[dict], bucket_name: str, folder_prefix: str = "archives/") -> dict:
    """Archives exported document snapshots in Google Cloud Storage."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or application default credentials are configured.
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    archived_files = []
    for record in document_records:
        document_id = record.get("document_id", "unknown_document")
        # Create a unique filename for the archive
        blob_name = f"{folder_prefix}{document_id}.json"
        blob = bucket.blob(blob_name)

        try:
            # Convert the record (dictionary) to a JSON string for storage
            record_content = json.dumps(record, indent=2)
            blob.upload_from_string(record_content, content_type='application/json')
            archived_files.append({
                "document_id": document_id,
                "status": "success",
                "gcs_uri": f"gs://{bucket_name}/{blob_name}"
            })
        except Exception as e:
            archived_files.append({"document_id": document_id, "status": "error", "message": str(e)})

    return {"status": "success", "archived_documents": archived_files}

if __name__ == '__main__':
    # This is a placeholder for local execution, not part of the core integration logic.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set and a GCS bucket exists.
    pass
