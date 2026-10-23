from google.cloud import storage

def image_asset_archive(bucket_name: str, file_name: str, data: bytes, content_type: str = "application/octet-stream"):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(data, content_type=content_type)
    return f"gs://{bucket_name}/{file_name}"

def archive_text_artifact(bucket_name: str, file_name: str, text_content: str):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(text_content, content_type="text/plain")
    return f"gs://{bucket_name}/{file_name}"
