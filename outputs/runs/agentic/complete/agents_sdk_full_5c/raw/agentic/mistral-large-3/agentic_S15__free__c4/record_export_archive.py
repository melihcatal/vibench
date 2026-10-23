import os
from typing import Dict, Any, List
from google.cloud import storage
import tempfile
import json

GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "your-export-bucket")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "your-google-credentials.json")

client = storage.Client()
bucket = client.bucket(GCS_BUCKET_NAME)

def export_documents_to_gcs(documents: List[Dict[str, Any]], archive_name: str) -> str:
    """
    Archives exported document snapshots in Google Cloud Storage.
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
        json.dump(documents, tmp_file)
        tmp_file_path = tmp_file.name
    
    blob = bucket.blob(f"exports/{archive_name}.json")
    blob.upload_from_filename(tmp_file_path)
    
    os.unlink(tmp_file_path)
    return f"gs://{GCS_BUCKET_NAME}/exports/{archive_name}.json"