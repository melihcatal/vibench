import os
import json
from google.cloud import storage
from google.api_core.exceptions import GoogleAPICallError

def archive_document(document_id: str, document_data: dict):
    """
    Archives a document snapshot in Google Cloud Storage.

    The client uses Application Default Credentials, which are typically configured
    by setting the GOOGLE_APPLICATION_CREDENTIALS environment variable.

    Args:
        document_id: The unique identifier for the document.
        document_data: A dictionary containing the document's data.
    """
    bucket_name = os.environ.get("GCS_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME environment variable is not set.")

    try:
        # Initialize the Google Cloud Storage client
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        # Define the blob (file) name and content
        destination_blob_name = f"archive/{document_id}.json"
        blob = bucket.blob(destination_blob_name)
        
        # Convert dict to JSON string for upload
        document_content = json.dumps(document_data, indent=2)

        # Upload the content
        blob.upload_from_string(
            document_content,
            content_type="application/json"
        )

        print(
            f"Document {document_id} was successfully archived to "
            f"gs://{bucket_name}/{destination_blob_name}"
        )

    except GoogleAPICallError as e:
        print(f"An error occurred with Google Cloud Storage: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
