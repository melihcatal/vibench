from google.cloud import storage
import os

def archive_metrics_snapshot(bucket_name: str, destination_blob_name: str, data: str) -> str:
    """Archives exported metric snapshots in Google Cloud Storage.

    Args:
        bucket_name: The name of your Cloud Storage bucket.
        destination_blob_name: The name of the file (blob) to create in the bucket.
        data: The content (e.g., JSON, CSV) of the metric snapshot to upload.

    Returns:
        A message indicating success or failure.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set up
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    try:
        blob.upload_from_string(data, content_type="application/json") # Assuming JSON data
        return f"Metric snapshot '{destination_blob_name}' uploaded to bucket '{bucket_name}'."
    except Exception as e:
        return f"Error archiving metric snapshot: {e}"

if __name__ == "__main__":
    # Example usage
    # Replace with your actual GCS bucket name
    gcs_bucket_name = os.environ.get("GCS_METRICS_ARCHIVE_BUCKET", "your-gcp-archive-bucket-name")
    snapshot_data_json = '''
{
  "timestamp": "2023-10-27T10:00:00Z",
  "metric": "cpu.utilization",
  "resource": "gce_instance-1",
  "values": [
    {"time": "2023-10-27T09:55:00Z", "value": 0.65},
    {"time": "2023-10-27T09:56:00Z", "value": 0.68},
    {"time": "2023-10-27T09:57:00Z", "value": 0.72}
  ]
}
'''
    import datetime
    timestamp_str = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    file_name = f"metric_snapshot_{timestamp_str}.json"

    print(f"Archiving metric snapshot to GCS bucket '{gcs_bucket_name}' as '{file_name}'...")
    result = archive_metrics_snapshot(gcs_bucket_name, file_name, snapshot_data_json)
    print(result)
