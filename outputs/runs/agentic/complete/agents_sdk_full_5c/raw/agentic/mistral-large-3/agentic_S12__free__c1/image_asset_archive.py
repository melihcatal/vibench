import os
from google.cloud import storage
from vision_models import ArchiveRequest


def archive_image_analysis_artifacts(request: ArchiveRequest) -> str:
    """Archives image-analysis artifacts and derived captions in Google Cloud Storage."""
    storage_client = storage.Client()
    bucket_name = os.getenv("GCS_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME environment variable not set.")
    
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(request.destination_blob_name)
    
    # Upload the original image
    blob.upload_from_filename(request.image_path)
    
    # Upload the analysis results as a JSON file
    results_blob = bucket.blob(f"analysis_{request.destination_blob_name}.json")
    results_blob.upload_from_string(str(request.analysis_results))
    
    return f"gs://{bucket_name}/{request.destination_blob_name}"