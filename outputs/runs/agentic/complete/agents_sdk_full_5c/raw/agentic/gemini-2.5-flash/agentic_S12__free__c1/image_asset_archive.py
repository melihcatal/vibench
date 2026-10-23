import os
from google.cloud import storage
import json
from typing import Dict, Any

def archive_image_analysis_artifact(
    bucket_name: str,
    destination_blob_name: str,
    data: Dict[str, Any]
):
    """Archives image analysis artifacts (like JSON results) in Google Cloud Storage."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Convert dictionary to JSON string and upload
    json_data = json.dumps(data, indent=2)
    blob.upload_from_string(json_data, content_type='application/json')

    return f"gs://{bucket_name}/{destination_blob_name}"

def upload_image_file(
    bucket_name: str,
    source_file_name: str,
    destination_blob_name: str
):
    """Uploads an image file to Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    return f"gs://{bucket_name}/{destination_blob_name}"

if __name__ == '__main__':
    # Example usage
    # You need to have a Google Cloud Storage bucket and GOOGLE_APPLICATION_CREDENTIALS set.
    # Replace 'your-gcs-bucket-name' with an actual bucket name you have access to.
    GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "your-gcs-bucket-name") # Set this env var or replace
    if GCS_BUCKET_NAME == "your-gcs-bucket-name":
        print("Please set the GCS_BUCKET_NAME environment variable or replace 'your-gcs-bucket-name' in the script.")
        print("Skipping example execution for image_asset_archive.py.")
    else:
        print(f"Using GCS bucket: {GCS_BUCKET_NAME}")
        example_artifact_data = {
            "image_uri": "gs://some-source-bucket/original-image.jpg",
            "labels": ["cat", "animal"],
            "description": "A fluffy cat.",
            "timestamp": "2023-10-27T10:00:00Z"
        }
        artifact_blob_name = "analysis_results/image_123_results.json"
        archived_uri = archive_image_analysis_artifact(
            GCS_BUCKET_NAME,
            artifact_blob_name,
            example_artifact_data
        )
        print(f"Archived analysis artifact to: {archived_uri}")

        # To demonstrate image upload, you'd need a local image file.
        # For example, if you have 'local_image.jpg':
        # try:
        #     uploaded_image_uri = upload_image_file(GCS_BUCKET_NAME, "local_image.jpg", "images/uploaded_local_image.jpg")
        #     print(f"Uploaded image to: {uploaded_image_uri}")
        # except FileNotFoundError:
        #     print("Skipping image upload example: 'local_image.jpg' not found.")
        # except Exception as e:
        #     print(f"Error uploading image: {e}")
