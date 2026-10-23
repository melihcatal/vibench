from google.cloud import storage

from observability_client import load_observability_config, storage_client


def metrics_export_archive(payload, config=None):
    config = load_observability_config(config)
    client = storage_client()
    bucket = client.bucket(payload["bucket"])
    blob = bucket.blob(payload["object_name"])
    blob.upload_from_string(payload["content"], content_type=payload.get("content_type", "application/json"))
    return {"bucket": bucket.name, "object_name": blob.name, "uri": f"gs://{bucket.name}/{blob.name}"}
