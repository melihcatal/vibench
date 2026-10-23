import os
from google.cloud import storage

def archive_document_snapshot(bucket_name: str, destination_blob_name: str, data: str) -> str:
    """
    Archives a document snapshot (as a string) to Google Cloud Storage.
    """
    # Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    try:
        blob.upload_from_string(data)
        public_url = blob.public_url
        print(f"Document snapshot archived to gs://{bucket_name}/{destination_blob_name}. Public URL: {public_url}")
        return public_url
    except Exception as e:
        print(f"Error archiving document snapshot to GCS: {e}")
        return f"Error: Could not archive document. {e}"

if __name__ == "__main__":
    # Set GOOGLE_APPLICATION_CREDENTIALS and GCS_BUCKET_NAME environment variables for testing
    
    gcs_bucket_name = os.environ.get("GCS_BUCKET_NAME")
    if not gcs_bucket_name:
        print("Please set the GCS_BUCKET_NAME environment variable.")
    else:
        document_content = '''{"id": "doc_export_123", "title": "Important Report", "date": "2023-10-27", "details": "This is a detailed report of the Q4 performance."}'''
        blob_path = "document_archives/important_report_20231027.json"

        try:
            archive_url = archive_document_snapshot(gcs_bucket_name, blob_path, document_content)
            print(f"Archival complete. URL: {archive_url}")
        except Exception as e:
            print(f"An error occurred during archival example: {e}")
