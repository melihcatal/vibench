import os
from vision_client import get_storage_client
from vision_models import normalize_archive_response

def image_asset_archive(image_bytes: bytes, bucket_name: str, blob_name: str, config: dict = None) -> dict:
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.upload_from_string(image_bytes, content_type="image/jpeg")  # Assuming JPEG, adjust as needed

    return normalize_archive_response(archive_status="completed", blob_name=blob_name)
