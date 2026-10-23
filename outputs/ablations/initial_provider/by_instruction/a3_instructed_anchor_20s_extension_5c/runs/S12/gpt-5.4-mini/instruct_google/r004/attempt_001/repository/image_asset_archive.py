import os
from typing import Any, Dict

from google.cloud import storage


def image_asset_archive(bucket_name: str, object_name: str, payload: Dict[str, Any]) -> str:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_string(str(payload), content_type="application/json")
    return f"gs://{bucket_name}/{object_name}"
