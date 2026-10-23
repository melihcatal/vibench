import os

from google.cloud import storage


def record_export_archive(name, payload):
    client = storage.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
    bucket = client.bucket(os.getenv("GCS_EXPORT_BUCKET"))
    blob = bucket.blob(name)
    blob.upload_from_string(payload if isinstance(payload, str) else str(payload))
    return {"provider": "google_cloud_storage", "object": f"gs://{bucket.name}/{name}"}
