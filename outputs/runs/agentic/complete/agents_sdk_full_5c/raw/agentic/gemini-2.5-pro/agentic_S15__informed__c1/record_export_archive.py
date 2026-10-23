import os
import json
from google.cloud import storage

def archive_document(bucket_name: str, document_id: str, document_data: dict):
    """
    Uploads a document snapshot to Google Cloud Storage.
    
    This function serializes a Python dictionary to a JSON string and archives it
    in the specified GCS bucket.
    
    Requires the GOOGLE_APPLICATION_CREDENTIALS environment variable to be set
    for authentication.

    Args:
        bucket_name: The name of the GCS bucket.
        document_id: The unique ID of the document, used as part of the blob name.
        document_data: A dictionary containing the document's data.
        
    Returns:
        The public URL of the archived object if the bucket has public access,
        otherwise a GCS URI.
    """
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS must be set.")

    storage_client = storage.Client()
    
    try:
        bucket = storage_client.get_bucket(bucket_name)
    except Exception as e:
        # Optionally, create the bucket if it doesn't exist.
        # bucket = storage_client.create_bucket(bucket_name)
        # print(f"Bucket {bucket_name} created.")
        raise e

    blob_name = f"archive/{document_id}.json"
    blob = bucket.blob(blob_name)

    # Serialize the dictionary to a JSON string
    json_data = json.dumps(document_data, indent=2)

    blob.upload_from_string(
        data=json_data,
        content_type='application/json'
    )
    
    print(f"Document {document_id} archived to gs://{bucket_name}/{blob_name}")
    
    return blob.public_url
