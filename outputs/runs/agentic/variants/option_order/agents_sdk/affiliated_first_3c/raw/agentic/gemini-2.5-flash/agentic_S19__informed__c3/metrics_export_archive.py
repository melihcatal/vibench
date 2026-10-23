import os
from google.cloud import storage
from datetime import datetime

def archive_metric_snapshot(bucket_name: str, file_content: str, destination_blob_name: str) -> str:
    """Archives exported metric snapshots in Google Cloud Storage.

    Args:
        bucket_name: The name of the GCS bucket.
        file_content: The content of the file to upload (e.g., JSON string of metric data).
        destination_blob_name: The name of the blob (object) in the bucket.

    Returns:
        The public URL of the uploaded object, or an error message.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    # The storage client automatically uses it if available.

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    try:
        blob.upload_from_string(file_content, content_type="application/json") # Assuming JSON content
        return f"gs://{bucket_name}/{destination_blob_name}"
    except Exception as e:
        return f"Error archiving snapshot: {e}"

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS and a GCS bucket to exist)
    # bucket_name = "your-gcs-bucket-name"
    # 
    # # Sample metric data as a JSON string
    # sample_metric_data_json = """
    # {
    #     "metricName": "cpu_utilization",
    #     "timestamp": "2023-10-27T10:30:00Z",
    #     "value": 0.75,
    #     "resource": {
    #         "type": "gce_instance",
    #         "labels": {"instance_id": "12345", "zone": "us-central1-a"}
    #     }
    # }
    # """
    # 
    # timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
    # blob_name = f"metric_snapshots/cpu_utilization_snapshot_{timestamp_str}.json"

    # if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ and bucket_name != "your-gcs-bucket-name":
    #     archive_url = archive_metric_snapshot(bucket_name, sample_metric_data_json, blob_name)
    #     print(f"Archived to: {archive_url}")
    # else:
    #     print("Please set GOOGLE_APPLICATION_CREDENTIALS and provide a valid GCS bucket name to run the example.")
    pass
