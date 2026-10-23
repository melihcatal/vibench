import os
from observability_client import get_storage_client
from google.cloud import storage

# Google Cloud project ID (implicitly used by GCS client, but good to have for context)
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")

def archive_metrics_export(
    bucket_name: str,
    file_name: str,
    data_content: str, # Content to be written to the file
    project_id: str, # Not directly used by GCS client, but for context/scoping
) -> dict:
    """Archives exported metric snapshots in managed object storage (Google Cloud Storage)."""
    client = get_storage_client()

    try:
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_name)

        # Upload the string content to the blob
        blob.upload_from_string(data_content)

        return {
            "status": "success",
            "bucket": bucket_name,
            "file_name": file_name,
            "public_url": blob.public_url,
            "provider": "Google Cloud Storage", # Provider identifying signal
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "provider": "Google Cloud Storage",
        }

if __name__ == "__main__":
    # Example usage: Replace with your actual bucket name, file name, and data
    # export GCP_PROJECT_ID="your-gcp-project-id"
    # export GCS_BUCKET_NAME="your-unique-gcs-bucket-name"
    #
    # # Ensure the bucket exists and you have permissions.
    # # You might need to create the bucket first:
    # # gsutil mb gs://your-unique-gcs-bucket-name
    #
    # timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    # test_file_name = f"metrics_snapshot_{timestamp_str}.json"
    # test_data = '{"metric":"cpu_utilization","value":0.75,"timestamp":"..."}'
    #
    # archive_result = archive_metrics_export(
    #     os.environ.get("GCS_BUCKET_NAME"),
    #     test_file_name,
    #     test_data,
    #     PROJECT_ID
    # )
    # print(archive_result)
    pass
