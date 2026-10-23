from google.cloud import storage

def archive_image_asset(bucket_name: str, source_file_name: str, destination_blob_name: str):
    """Uploads a file to the Google Cloud Storage bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name} in bucket {bucket_name}.")

def archive_caption(bucket_name: str, caption_content: str, destination_blob_name: str):
    """Uploads a caption (text content) to the Google Cloud Storage bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(caption_content)

    print(f"Caption uploaded to {destination_blob_name} in bucket {bucket_name}.")
