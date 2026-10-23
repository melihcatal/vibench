
import os
from google.cloud import storage
from datetime import datetime

def archive_metric_snapshot(bucket_name: str, file_content: str, destination_blob_name: str = None) -> str:
    """
    Archives exported metric snapshots in Google Cloud Storage.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set up.

    Args:
        bucket_name (str): The name of your GCS bucket.
        file_content (str): The content of the metric snapshot (e.g., JSON or CSV string).
        destination_blob_name (str): The path and name for the blob in the bucket (e.g., "metrics/daily_snapshot_2023-10-27.json").
                                     If None, a default name based on timestamp will be generated.

    Returns:
        str: A message indicating success or failure, including the public URL of the archived file.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    if destination_blob_name is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        destination_blob_name = f"metrics/snapshot_{timestamp}.json"

    blob = bucket.blob(destination_blob_name)

    try:
        blob.upload_from_string(file_content, content_type="application/json")
        return f"Metric snapshot archived successfully to gs://{bucket_name}/{destination_blob_name}"
    except Exception as e:
        return f"Error archiving metric snapshot to GCS: {e}"

if __name__ == "__main__":
    bucket_name = os.environ.get("GCP_BUCKET_NAME", "your-gcs-bucket-name")
    
    # Example metric snapshot content (e.g., JSON representation of metric data)
    example_snapshot_content = '''
{
    "timestamp": "2023-10-27T10:30:00Z",
    "metric_name": "compute.googleapis.com/instance/cpu/utilization",
    "data_points": [
        {"instance_id": "inst-1", "value": 0.45},
        {"instance_id": "inst-2", "value": 0.62}
    ]
}
'''

    archive_status = archive_metric_snapshot(bucket_name, example_snapshot_content)
    print(archive_status)

    # Example with a custom blob name
    custom_blob_name = "metrics/manual_export_cpu_2023-10-27.json"
    archive_status_custom = archive_metric_snapshot(bucket_name, example_snapshot_content, custom_blob_name)
    print(archive_status_custom)
