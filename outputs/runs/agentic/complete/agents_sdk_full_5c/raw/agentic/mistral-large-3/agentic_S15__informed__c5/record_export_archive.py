import os
from typing import Dict, Any
from datetime import datetime
from google.cloud import storage

def archive_document(document: Dict[str, Any], bucket_name: str) -> str:
    """
    Archives a document snapshot in Google Cloud Storage.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    
    document_id = document.get("id", "unknown")
    timestamp = datetime.utcnow().isoformat()
    blob_name = f"exports/{document_id}_{timestamp}.json"
    
    blob = bucket.blob(blob_name)
    blob.upload_from_string(data=str(document), content_type="application/json")
    
    return f"gs://{bucket_name}/{blob_name}"