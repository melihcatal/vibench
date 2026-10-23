from storage_client import get_gcs_client, get_bucket_name

def upload_to_gcs(source_file_path: str, destination_blob_name: str):
    """
    Uploads a file to a Google Cloud Storage bucket.

    Args:
        source_file_path (str): The local path to the file to upload.
        destination_blob_name (str): The desired name of the object in GCS.

    Returns:
        The public URL of the uploaded object.
    """
    client = get_gcs_client()
    bucket_name = get_bucket_name()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_path)

    print(
        f"File {source_file_path} uploaded to {destination_blob_name} in bucket {bucket_name}."
    )
    return blob.public_url

