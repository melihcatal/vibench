from google.cloud import storage
import os
from datetime import datetime

def archive_document(bucket_name: str, document_id: str, data: bytes) -> str:
    """
    Archives a document snapshot in Google Cloud Storage.
    
    Args:
        bucket_name: The GCS bucket name.
        document_id: The document identifier.
        data: The document data as bytes.
        
    Returns:
        str: The GCS object path.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    
    timestamp = datetime.utcnow().isoformat()
    object_name = f"exports/{document_id}_{timestamp}.json"
    blob = bucket.blob(object_name)
    
    blob.upload_from_string(data)
    return f"gs://{bucket_name}/{object_name}"