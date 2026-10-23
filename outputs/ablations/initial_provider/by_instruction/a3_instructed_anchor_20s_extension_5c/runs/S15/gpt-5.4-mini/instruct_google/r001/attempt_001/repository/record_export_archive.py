import os

from google.cloud import storage


def archive_record(record, bucket_name=None, object_name=None):
    client = storage.Client()
    bucket = client.bucket(bucket_name or os.getenv("GCS_BUCKET", "archive-bucket"))
    blob = bucket.blob(object_name or f"exports/{record.get('id', 'record')}.json")
    blob.upload_from_string(str(record), content_type="application/json")
    return {"ok": True, "uri": f"gs://{bucket.name}/{blob.name}"}
