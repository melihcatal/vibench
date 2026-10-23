import os
from google.cloud import storage

def image_asset_archive(payload, config=None):
    config = config or {}

    client = storage.Client()

    bucket_name = config.get('bucket_name')
    if not bucket_name:
        raise ValueError("'bucket_name' must be provided in config.")

    file_name = payload.get('file_name')
    file_content = payload.get('file_content') # This could be image bytes, JSON of analysis, etc.
    content_type = payload.get('content_type', 'application/octet-stream')

    if not file_name or not file_content:
        raise ValueError("'file_name' and 'file_content' must be provided in payload.")

    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Upload the file content
    blob.upload_from_string(file_content, content_type=content_type)

    return {'archive_uri': f"gs://{bucket_name}/{file_name}"}
