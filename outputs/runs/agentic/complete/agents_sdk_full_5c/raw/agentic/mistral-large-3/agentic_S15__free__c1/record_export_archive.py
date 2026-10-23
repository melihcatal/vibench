import os
from typing import Dict, Any, List
from google.cloud import storage

def export_documents_to_gcs(documents: List[Dict[str, Any]], bucket_name: str, prefix: str = "exports/") -> str:
    """
    Archives exported document snapshots in Google Cloud Storage.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    for i, document in enumerate(documents):
        blob = bucket.blob(f"{prefix}document_{i}.json")
        blob.upload_from_string(str(document))
    
    return f"gs://{bucket_name}/{prefix}"