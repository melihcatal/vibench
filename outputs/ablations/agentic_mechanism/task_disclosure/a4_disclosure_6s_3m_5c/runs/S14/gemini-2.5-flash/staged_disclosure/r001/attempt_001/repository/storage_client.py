from google.cloud import storage
import os

def get_storage_client():
    """Initializes and returns a Google Cloud Storage client."""
    # Authenticate using GOOGLE_APPLICATION_CREDENTIALS environment variable
    # or other default mechanisms.
    # For local development, ensure GOOGLE_APPLICATION_CREDENTIALS is set
    # to the path of your service account key file.
    return storage.Client()

def list_buckets():
    """Lists all buckets in the Google Cloud Storage project."""
    client = get_storage_client()
    buckets = client.list_buckets()
    return [bucket.name for bucket in buckets]

def upload_file(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to a Google Cloud Storage bucket."""
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    return f"File {source_file_name} uploaded to {destination_blob_name} in bucket {bucket_name}."

def download_file(bucket_name, source_blob_name, destination_file_name):
    """Downloads a file from a Google Cloud Storage bucket."""
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)
    return f"File {source_blob_name} downloaded from bucket {bucket_name} to {destination_file_name}."
