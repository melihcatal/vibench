import os

from google.cloud import storage


def archive_record_snapshot(bucket_name, object_name, data):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_string(data if isinstance(data, str) else str(data), content_type="application/json")
    return {"bucket": bucket_name, "object": object_name}
