import os
from datetime import datetime
from google.cloud import storage

def archive_metrics_snapshot(
    bucket_name: str,
    destination_blob_name: str,
    data: str,
    content_type: str = "application/json",
) -> str:
    """Archives exported metric snapshots in Google Cloud Storage.

    Args:
        bucket_name: The name of your Cloud Storage bucket.
        destination_blob_name: The name of the blob (object) to create in the bucket.
        data: The content of the metric snapshot to upload.
        content_type: The MIME type of the content (e.g., "application/json", "text/csv").

    Returns:
        The public URL of the uploaded blob, or an empty string on failure.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    try:
        blob.upload_from_string(data, content_type=content_type)
        return blob.public_url
    except Exception as e:
        print(f"Error archiving metric snapshot to GCS: {e}")
        return ""

if __name__ == '__main__':
    print("--- Archiving Metric Snapshots to Google Cloud Storage ---")
    # Replace with your actual bucket name
    gcs_bucket_name = os.environ.get("GCS_BUCKET_NAME", "your-gcs-bucket-name") # Placeholder
    if gcs_bucket_name == "your-gcs-bucket-name":
        print("Warning: GCS_BUCKET_NAME environment variable not set. Using placeholder bucket name.\nPlease set it to your actual bucket name.")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"metric_snapshot_{timestamp}.json"
    snapshot_data = "{\"metric\": \"cpu_utilization\", \"value\": 0.75, \"timestamp\": \"2023-10-27T10:30:00Z\"}"

    print(f"Attempting to upload \'{file_name}\' to bucket \'{gcs_bucket_name}\'...")
    uploaded_url = archive_metrics_snapshot(gcs_bucket_name, file_name, snapshot_data)

    if uploaded_url:
        print(f"Metric snapshot archived successfully. Public URL: {uploaded_url}")
    else:
        print("Failed to archive metric snapshot.")
        print("Note: Ensure GOOGLE_APPLICATION_CREDENTIALS are set up and the bucket exists and is accessible.")
