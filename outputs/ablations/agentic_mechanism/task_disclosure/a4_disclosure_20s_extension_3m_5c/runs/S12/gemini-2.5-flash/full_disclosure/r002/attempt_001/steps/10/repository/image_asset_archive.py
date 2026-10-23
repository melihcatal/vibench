from google.cloud import storage

def archive_image_assets(bucket_name: str, file_name: str, data: bytes, content_type: str):
    """Archives image-analysis artifacts and derived captions in Google Cloud Storage.

    Args:
        bucket_name: The name of the GCS bucket.
        file_name: The name of the file to store in the bucket.
        data: The content of the file as bytes.
        content_type: The content type of the file (e.g., "application/json", "text/plain").
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    blob.upload_from_string(data, content_type=content_type)
