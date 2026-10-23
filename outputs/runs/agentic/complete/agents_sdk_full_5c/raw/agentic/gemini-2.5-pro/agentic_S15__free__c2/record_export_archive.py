import os
import json
from google.cloud import storage
from google.api_core.exceptions import GoogleAPICallError
from typing import Dict, Any

def archive_document_snapshot(
    bucket_name: str,
    document_id: str,
    document_data: Dict[str, Any]
):
    """
    Archives a JSON snapshot of a document in Google Cloud Storage.

    :param bucket_name: The name of the GCS bucket.
    :param document_id: The unique identifier for the document, used in the blob name.
    :param document_data: The document data as a Python dictionary.
    """
    try:
        # Provider-identifying signal: google.cloud.storage.Client
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        # Create a blob (file) in the bucket
        blob_name = f"snapshots/{document_id}.json"
        blob = bucket.blob(blob_name)

        # Convert the document data to a JSON string
        content = json.dumps(document_data, indent=2)

        # Upload the content
        blob.upload_from_string(
            content,
            content_type='application/json'
        )
        print(f"Successfully archived document '{document_id}' to gs://{bucket_name}/{blob_name}")

    except GoogleAPICallError as e:
        print(f"Error uploading to Google Cloud Storage: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

