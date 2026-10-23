from google.cloud.storage import Bucket
from storage_client import get_storage_client, get_default_bucket_name

def upload_file_to_gcs(source_file_path: str, destination_blob_name: str):
    """
    Uploads a file to a Google Cloud Storage bucket.

    Args:
        source_file_path (str): The path to the file to upload.
        destination_blob_name (str): The name of the blob in the bucket.
    """
    client = get_storage_client()
    bucket_name = get_default_bucket_name()
    bucket: Bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_path)

    print(f"File {source_file_path} uploaded to {bucket_name}/{destination_blob_name}.")
