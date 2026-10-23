import os
from google.cloud import storage


def image_asset_archive(payload, config=None):
    config = config or {}
    client = storage.Client()
    bucket = client.bucket(config.get("bucket") or os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET", ""))
    blob = bucket.blob(config.get("object_name") or payload.get("object_name", "image-asset.json"))
    blob.upload_from_string(payload.get("content", ""), content_type="application/json")
    return {"bucket": bucket.name, "object_name": blob.name}
