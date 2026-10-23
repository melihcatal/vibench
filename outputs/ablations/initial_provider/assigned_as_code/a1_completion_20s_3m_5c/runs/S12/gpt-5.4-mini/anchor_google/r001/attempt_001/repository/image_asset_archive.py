import os
from google.cloud import storage


def image_asset_archive(payload, config=None):
    config = config or {}
    client = storage.Client()
    bucket = client.bucket(config.get("bucket") or os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET"))
    prefix = config.get("prefix", "image-analysis")
    artifact_name = config.get("artifact_name", "analysis.json")
    blob = bucket.blob(f"{prefix}/{artifact_name}")
    blob.upload_from_string(payload.get("content", ""), content_type="application/json")
    return {"uri": f"gs://{bucket.name}/{blob.name}"}
