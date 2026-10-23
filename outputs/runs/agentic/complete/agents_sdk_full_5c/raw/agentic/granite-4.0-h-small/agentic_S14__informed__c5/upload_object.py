import os
from google.cloud import storage

def upload_object(bucket_name, source_path, destination_blob_name):
    """Upload a file or byte stream to Google Cloud Storage.

    bucket_name: str - name of the GCS bucket
    source_path: str or bytes - path to local file or bytes to upload
    destination_blob_name: str - name of the object in GCS
    """
    # Create/ get client using env var GOOGLE_APPLICATION_CREDENTIALS
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    if isinstance(source_path, bytes):
        blob.upload_from_string(source_path)
    else:
        blob.upload_from_filename(source_path)
    print(f"Uploaded {source_path} to gs://{bucket_name}/{destination_blob_name}")
