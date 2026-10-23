from google.cloud import storage


def metrics_export_archive(payload, config=None):
    cfg = config or {}
    client = storage.Client()
    bucket = client.bucket(cfg["bucket"])
    blob = bucket.blob(payload["archive_path"])
    blob.upload_from_string(payload["content"], content_type=payload.get("content_type", "application/json"))
    return {"bucket": cfg["bucket"], "archive_path": payload["archive_path"], "provider": "google.cloud.storage"}
