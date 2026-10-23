from google.cloud import storage
from observability_client import get_storage_client, get_project_id
import json


def archive_metric_snapshot(
    bucket_name: str, destination_blob_name: str, metric_data: dict
) -> str:
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Convert metric data to JSON string for storage
    metric_data_json = json.dumps(metric_data, indent=2)

    blob.upload_from_string(metric_data_json, content_type="application/json")

    return f"gs://{bucket_name}/{destination_blob_name}"


if __name__ == "__main__":
    # IMPORTANT: Replace with an existing GCS bucket name in your project
    # Ensure the service account has 'Storage Object Admin' or 'Storage Object Creator' role.
    test_bucket_name = "your-gcs-bucket-name"
    test_blob_name = "metric_snapshots/cpu_utilization_2023-03-15.json"

    # Example metric data to archive
    example_metric_data = {
        "metric_type": "compute.googleapis.com/instance/cpu/utilization",
        "timestamp": "2023-03-15T12:00:00Z",
        "value": 0.75,
        "resource_labels": {"instance_id": "1234567890", "zone": "us-central1-a"},
    }

    try:
        archive_url = archive_metric_snapshot(
            test_bucket_name, test_blob_name, example_metric_data
        )
        print(f"Metric snapshot archived to: {archive_url}")
    except Exception as e:
        print(f"Error archiving metric snapshot: {e}")
        print(
            f"Please ensure the bucket '{test_bucket_name}' exists and your credentials have access."
        )
