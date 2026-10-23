
from google.cloud import storage
import os

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

if __name__ == '__main__':
    # Replace with your actual bucket name and file paths
    # For example:
    # BUCKET_NAME = "my-metric-archive-bucket"
    # LOCAL_FILE_PATH = "metrics_snapshot_2026-09-20.json"
    # DESTINATION_BLOB_NAME = "snapshots/metrics_snapshot_2026-09-20.json"

    # Example usage (uncomment and modify with your details):
    # if os.path.exists(LOCAL_FILE_PATH):
    #     upload_blob(BUCKET_NAME, LOCAL_FILE_PATH, DESTINATION_BLOB_NAME)
    # else:
    #     print(f"Error: Local file not found at {LOCAL_FILE_PATH}")
