from typing import Any, Dict

from google.cloud import storage


def metrics_export_archive(
    bucket_name: str, object_name: str, content: bytes
) -> Dict[str, Any]:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_string(content)
    return {"bucket": bucket_name, "object": object_name}
