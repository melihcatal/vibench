import uuid

from google.cloud import storage

from observability_client import storage_client


def metrics_export_archive(payload, config=None):
    client = storage_client()
    bucket = client.bucket(payload["bucket"])
    blob_name = payload.get("blob_name") or f"metric-archive-{uuid.uuid4().hex}.json"
    blob = bucket.blob(blob_name)
    blob.upload_from_string(payload["content"], content_type="application/json")
    return {"bucket": payload["bucket"], "blob_name": blob_name, "gs_uri": f"gs://{payload['bucket']}/{blob_name}"}
