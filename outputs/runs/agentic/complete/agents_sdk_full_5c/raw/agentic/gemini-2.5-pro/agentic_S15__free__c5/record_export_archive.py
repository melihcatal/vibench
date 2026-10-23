import json
from google.cloud import storage

def archive_document(bucket_name: str, document: dict, destination_blob_name: str):
    """
    Uploads a document to a Google Cloud Storage bucket as a JSON file.

    Authentication is handled automatically by the client library via the
    GOOGLE_APPLICATION_CREDENTIALS environment variable.

    Provider: Google Cloud Storage
    """
    # Provider-identifying signal: google.cloud.storage.Client
    storage_client = storage.Client()
    
    try:
        bucket = storage_client.get_bucket(bucket_name)
    except Exception as e:
        print(f"Error accessing bucket {bucket_name}: {e}")
        raise

    blob = bucket.blob(destination_blob_name)

    # Convert the document dictionary to a JSON string for upload.
    document_json = json.dumps(document, indent=2)

    blob.upload_from_string(
        document_json,
        content_type='application/json'
    )

    print(f"Document {destination_blob_name} successfully archived in bucket {bucket_name}.")
    
    # Return the full GCS path to the archived object.
    return f"gs://{bucket_name}/{destination_blob_name}"
