from google.cloud import storage

def upload_to_gcs(bucket_name: str, blob_name: str, data: bytes, content_type: str = "application/octet-stream") -> str:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(data, content_type=content_type)
    return f"gs://{bucket_name}/{blob_name}"

def upload_string_to_gcs(bucket_name: str, blob_name: str, content: str, content_type: str = "text/plain") -> str:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(content, content_type=content_type)
    return f"gs://{bucket_name}/{blob_name}"
