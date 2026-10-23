import os
from google.cloud import storage


def archive_metric_snapshot(
    bucket_name: str, destination_blob_name: str, data: str
) -> str:
    """Archives exported metric snapshots in managed object storage using Google Cloud Storage."""
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data)

    return f"gs://{bucket_name}/{destination_blob_name}"


# Example usage (assuming GOOGLE_APPLICATION_CREDENTIALS is set and BUCKET_NAME is configured)
# if __name__ == "__main__":
#     bucket_name = os.environ.get("GCS_BUCKET_NAME", "your-gcs-bucket-name")
#     snapshot_data = "{\"metric\": \"cpu_utilization\", \"timestamp\": \"2023-10-27T10:00:00Z\", \"value\": 0.75}"
#     blob_name = "metric-snapshots/cpu_utilization_2023-10-27-10-00.json"
#     archive_url = archive_metric_snapshot(bucket_name, blob_name, snapshot_data)
#     print(f"Archived metric snapshot to: {archive_url}")
