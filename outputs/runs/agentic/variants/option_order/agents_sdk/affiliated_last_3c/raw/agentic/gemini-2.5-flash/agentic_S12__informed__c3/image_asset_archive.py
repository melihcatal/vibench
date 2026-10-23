import os
from google.cloud import storage
from datetime import datetime

def archive_image_analysis_artifact(
    bucket_name: str, 
    source_blob_name: str, 
    data_bytes: bytes, 
    content_type: str = "application/json"
) -> str:
    """
    Archives image analysis artifacts (e.g., JSON results, derived captions)
    in Google Cloud Storage.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    # Generate a unique blob name for the archive
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_blob_name = f"analysis_artifacts/{source_blob_name}_{timestamp}.json" # Assuming JSON for general artifacts

    blob = bucket.blob(archive_blob_name)
    blob.upload_from_string(data_bytes, content_type=content_type)

    return blob.public_url # Or blob.name if public URL is not needed

if __name__ == '__main__':
    # This example requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    # bucket = "your-gcs-bucket-name"
    # source_id = "image_123"
    # artifact_data = '{"labels": ["cat"], "description": "A cat."}'.encode('utf-8')
    # archived_url = archive_image_analysis_artifact(bucket, source_id, artifact_data)
    # print(f"Archived artifact URL: {archived_url}")
    pass
