import os
from google.cloud import storage
from typing import Dict, Any

def archive_document_snapshot(bucket_name: str, destination_blob_name: str, data: Dict[str, Any]):
    """
    Archives exported document snapshots or attachments in Google Cloud Storage.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set in the environment.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # For a snapshot, we might store it as a JSON string
    import json
    json_data = json.dumps(data, indent=2)
    blob.upload_from_string(json_data, content_type="application/json")

    return {"status": "success", "bucket": bucket_name, "blob": destination_blob_name, "uri": blob.public_url}

if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS env var and a GCS bucket)
    # from database_models import Document

    # sample_data = Document("doc_archive_1", {"summary": "Archived content", "date": "2023-10-27"}).to_dict()
    # gcs_bucket_name = os.environ.get("GCS_ARCHIVE_BUCKET") # Or your actual bucket name

    # if gcs_bucket_name:
    #     response = archive_document_snapshot(gcs_bucket_name, "archive/doc_archive_1.json", sample_data)
    #     print(f"Archiving response: {response}")
    # else:
    #     print("Please set the GCS_ARCHIVE_BUCKET environment variable.")
    print("To run this example, ensure GOOGLE_APPLICATION_CREDENTIALS and GCS_ARCHIVE_BUCKET are set and uncomment the example usage.")
