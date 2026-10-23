"""[LATER-STEP] Archive image-analysis artifacts and derived captions in managed object storage"""
from google.cloud import storage
import json
from typing import Dict, Any

def image_asset_archive(artifacts: Dict[str, Any], bucket_name: str, object_name: str) -> None:
    # Google Cloud Storage
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_string(
        data=json.dumps(artifacts, indent=2),
        content_type='application/json'
    )
