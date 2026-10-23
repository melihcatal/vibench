import os
import json
from google.cloud import storage

def archive_document(bucket_name: str, blob_name: str, document_data: dict):
    """
    Archives a document snapshot in Google Cloud Storage.
    The client automatically uses credentials from the GOOGLE_APPLICATION_CREDENTIALS
    environment variable.

    :param bucket_name: The name of the GCS bucket.
    :param blob_name: The name for the new blob (file) in the bucket.
    :param document_data: The document data to serialize and upload.
    """
    try:
        # Instantiates a client.
        storage_client = storage.Client()

        # Get the bucket
        bucket = storage_client.bucket(bucket_name)

        # Create a new blob
        blob = bucket.blob(blob_name)

        # Serialize the document data to a JSON string
        document_content = json.dumps(document_data, indent=2)

        # Upload the content
        blob.upload_from_string(document_content, content_type='application/json')

        print(f"Document {blob_name} uploaded to bucket {bucket_name}.")

    except Exception as e:
        print(f"Failed to upload to Google Cloud Storage: {e}")
        raise
