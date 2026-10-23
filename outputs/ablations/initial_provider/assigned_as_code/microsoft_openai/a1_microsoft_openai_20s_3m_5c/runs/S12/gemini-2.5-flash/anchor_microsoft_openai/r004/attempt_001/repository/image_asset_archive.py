from google.cloud import storage
import os

def image_asset_archive(payload, config=None):
    config = config or {}
    storage_client = storage.Client()

    bucket_name = config.get('gcs_bucket_name', os.environ.get('GCS_BUCKET_NAME'))
    destination_blob_name = payload.get('file_name', 'image_archive.bin')
    content_to_archive = payload.get('content', b'')
    content_type = payload.get('content_type', 'application/octet-stream')

    if not bucket_name:
        raise ValueError("Google Cloud Storage bucket name not provided.")

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(content_to_archive, content_type=content_type)

    return {'archive_url': f"gs://{bucket_name}/{destination_blob_name}"}
