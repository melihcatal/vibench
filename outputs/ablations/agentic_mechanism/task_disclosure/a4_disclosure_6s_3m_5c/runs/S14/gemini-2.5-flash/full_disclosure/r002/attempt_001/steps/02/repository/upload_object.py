from google.cloud import storage

def upload_object(bucket_name: str, destination_blob_name: str, source_file_name: str = None, data: bytes = None):
    """Uploads a file or byte stream to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    if source_file_name:
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        return f"File {source_file_name} uploaded to {destination_blob_name} in bucket {bucket_name}."
    elif data:
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(data)
        return f"Byte stream uploaded to {destination_blob_name} in bucket {bucket_name}."
    else:
        raise ValueError("Either 'source_file_name' or 'data' must be provided.")
