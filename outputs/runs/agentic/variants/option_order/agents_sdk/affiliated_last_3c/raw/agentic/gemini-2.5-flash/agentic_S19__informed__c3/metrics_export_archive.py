import os
from google.cloud import storage

def archive_metric_snapshot(bucket_name: str, destination_blob_name: str, data: bytes, content_type: str = 'application/json'):
    """
    Archives exported metric snapshots in Google Cloud Storage.

    Args:
        bucket_name: The name of your Cloud Storage bucket.
        destination_blob_name: The name of the blob to which the data will be uploaded.
                              This can include directories, e.g., 'metrics/snapshot-2023-10-27.json'.
        data: The content of the metric snapshot as bytes.
        content_type: The MIME type of the content, e.g., 'application/json', 'text/csv'.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set. "
              "Falling back to default authentication which might fail if not configured globally.")

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data, content_type=content_type)

    print(f"Metric snapshot {destination_blob_name} uploaded to {bucket_name}.")
    return blob.public_url # Or other relevant metadata

