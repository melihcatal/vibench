from google.cloud import storage
import json


def archive_image_analysis_artifacts(
    bucket_name: str,
    destination_blob_name: str,
    image_content_bytes: bytes,
    analysis_results: dict,
    alt_text: str,
):
    """Archives image assets and analysis results in Google Cloud Storage.

    Args:
        bucket_name: The name of the GCS bucket.
        destination_blob_name: The path/name for the image in the bucket.
        image_content_bytes: The raw bytes of the image file.
        analysis_results: A dictionary containing the full analysis results.
        alt_text: The generated and potentially translated alt text.
    """
    # Provider: Google Cloud Storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Archive original image
    image_blob = bucket.blob(destination_blob_name)
    image_blob.upload_from_string(
        image_content_bytes, content_type="image/jpeg"
    )  # Assuming JPEG

    # Archive analysis results as JSON
    analysis_blob_name = f"{destination_blob_name}.analysis.json"
    analysis_blob = bucket.blob(analysis_blob_name)
    analysis_blob.upload_from_string(
        json.dumps(analysis_results, indent=2),
        content_type="application/json",
    )

    # Archive alt text as a text file
    alt_text_blob_name = f"{destination_blob_name}.alt_text.txt"
    alt_text_blob = bucket.blob(alt_text_blob_name)
    alt_text_blob.upload_from_string(
        alt_text,
        content_type="text/plain",
    )
