import os
from vision_client import get_gcs_client
from google.cloud.storage import Client, Blob


def archive_image_analysis_artifacts(
    bucket_name: str, destination_blob_name: str, data: str
) -> str:
    client = get_gcs_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data)

    return f"gs://{bucket_name}/{destination_blob_name}"


if __name__ == "__main__":
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    # Replace with your GCS bucket name and desired blob name.
    # For testing, you might need to create a dummy bucket and ensure proper permissions.
    gcs_bucket_name = os.environ.get("GCS_BUCKET_NAME", "your-gcs-bucket-name")
    gcs_blob_name = "image_analysis_artifacts/example_image_analysis.json"
    analysis_data = '{"image_id": "123", "labels": ["cat"], "description": "A cat."}'

    try:
        archived_uri = archive_image_analysis_artifacts(
            gcs_bucket_name, gcs_blob_name, analysis_data
        )
        print(f"Image analysis artifacts archived to: {archived_uri}")
    except Exception as e:
        print(f"Error archiving artifacts: {e}")
        print(
            "Please ensure GOOGLE_APPLICATION_CREDENTIALS is set and GCS_BUCKET_NAME is a valid, existing bucket with write permissions."
        )
