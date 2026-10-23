import os
from typing import Dict, List
from google.cloud import storage


def archive_image_analysis_artifacts(
    image_path: str, analysis_results: Dict, destination_blob_name: str
) -> str:
    """
    Archives image-analysis artifacts and derived captions in Google Cloud Storage.
    """
    client = storage.Client()
    bucket_name = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
    bucket = client.bucket(bucket_name)

    # Upload image
    image_blob = bucket.blob(f"images/{destination_blob_name}")
    image_blob.upload_from_filename(image_path)

    # Upload analysis results
    results_blob = bucket.blob(f"analysis/{destination_blob_name}.json")
    results_blob.upload_from_string(str(analysis_results))

    return f"gs://{bucket_name}/analysis/{destination_blob_name}.json"
