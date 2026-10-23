import os
import json
from google.cloud import storage


def archive_image_artifacts(
    bucket_name: str,
    base_blob_name: str,
    image_content: bytes,
    analysis_results: dict,
    derived_captions: str,
):
    """
    Archives image analysis artifacts to Google Cloud Storage.

    Args:
        bucket_name: The name of the GCS bucket.
        base_blob_name: The base name for the stored objects (e.g., 'image-abc').
        image_content: The raw binary content of the image file.
        analysis_results: A dictionary of analysis results to be stored as JSON.
        derived_captions: A string of captions or descriptions to be stored as a text file.
    """
    # Assumes GOOGLE_APPLICATION_CREDENTIALS is set
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # 1. Upload the original image
    image_blob = bucket.blob(f"{base_blob_name}.jpg")
    image_blob.upload_from_string(image_content, content_type="image/jpeg")
    print(f"Uploaded image to gs://{bucket_name}/{base_blob_name}.jpg")

    # 2. Upload the analysis results as a JSON file
    analysis_blob = bucket.blob(f"{base_blob_name}_analysis.json")
    analysis_blob.upload_from_string(
        json.dumps(analysis_results, indent=2), content_type="application/json"
    )
    print(f"Uploaded analysis to gs://{bucket_name}/{base_blob_name}_analysis.json")

    # 3. Upload the derived captions as a text file
    captions_blob = bucket.blob(f"{base_blob_name}_captions.txt")
    captions_blob.upload_from_string(derived_captions, content_type="text/plain")
    print(f"Uploaded captions to gs://{bucket_name}/{base_blob_name}_captions.txt")
