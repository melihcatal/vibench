import os
from google.cloud import storage
from storage_client import get_storage_client

def upload_object(bucket_name, source_path, destination_blob_name):
    """Upload a file or byte stream to Google Cloud Storage.
    Args:
        bucket_name (str): Name of the bucket.
        source_path (str): Path to local file or '-' for stdin.
        destination_blob_name (str): Name of the object in bucket.
    """
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    if source_path == '-':
        content = os.fdopen(0).read()  # read from stdin
    else:
        with open(source_path, 'rb') as f:
            content = f.read()
    blob.upload_from_string(content)
    print(f'Uploaded {source_path} to gs://{bucket_name}/{destination_blob_name}')