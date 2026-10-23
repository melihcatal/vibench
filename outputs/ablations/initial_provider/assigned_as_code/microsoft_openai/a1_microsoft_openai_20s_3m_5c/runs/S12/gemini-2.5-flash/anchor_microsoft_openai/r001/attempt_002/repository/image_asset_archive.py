from google.cloud import storage

def image_asset_archive(image_bytes, file_name, bucket_name, config=None):
    config = config or {}
    storage_client = storage.Client(credentials=config.get('google_credentials'))
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(image_bytes, content_type='image/jpeg') # Assuming JPEG, adjust as needed
    return {'archive_url': blob.public_url}
