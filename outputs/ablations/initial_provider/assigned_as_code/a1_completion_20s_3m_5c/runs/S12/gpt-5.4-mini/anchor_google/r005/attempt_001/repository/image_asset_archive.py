import os

from google.cloud import storage


def image_asset_archive(payload, config=None):
    config = config or {}
    client = storage.Client()
    bucket = client.bucket(config.get("bucket") or os.getenv("GCS_BUCKET"))
    blob = bucket.blob(config.get("object_name") or payload.get("object_name", "image-analysis.json"))
    blob.upload_from_string(payload.get("artifact_json", "{}"), content_type="application/json")
    return {"uri": f"gs://{bucket.name}/{blob.name}"}
