from google.cloud import storage
import os
from typing import Dict, Any

def archive_analysis_artifacts(
    bucket_name: str,
    image_id: str,
    original_image_content: bytes,
    analysis_results: Dict[str, Any],
    alt_text_translations: Dict[str, str] = None,
    summary_text: str = None
):
    """
    Archives image-analysis artifacts and derived captions in Google Cloud Storage.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Archive original image
    image_blob = bucket.blob(f"{image_id}/original_image.jpg")
    image_blob.upload_from_string(original_image_content, content_type="image/jpeg")
    print(f"Archived original image to gs://{bucket_name}/{image_id}/original_image.jpg")

    # Archive analysis results (as JSON)
    analysis_results_blob = bucket.blob(f"{image_id}/analysis_results.json")
    analysis_results_blob.upload_from_string(
        str(analysis_results), # Convert dict to string for simple upload
        content_type="application/json"
    )
    print(f"Archived analysis results to gs://{bucket_name}/{image_id}/analysis_results.json")

    # Archive translated alt texts
    if alt_text_translations:
        alt_text_blob = bucket.blob(f"{image_id}/alt_text_translations.json")
        alt_text_blob.upload_from_string(
            str(alt_text_translations), # Convert dict to string
            content_type="application/json"
        )
        print(f"Archived alt text translations to gs://{bucket_name}/{image_id}/alt_text_translations.json")

    # Archive summary text
    if summary_text:
        summary_blob = bucket.blob(f"{image_id}/summary.txt")
        summary_blob.upload_from_string(summary_text, content_type="text/plain")
        print(f"Archived summary text to gs://{bucket_name}/{image_id}/summary.txt")

if __name__ == '__main__':
    # Example usage
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"
    # BUCKET_NAME = "your-gcs-bucket-name"
    # IMAGE_ID = "test-image-123"
    #
    # # Dummy content for example
    # dummy_image_content = b"fake_image_bytes_here"
    # dummy_analysis = {"labels": ["car"], "description": "a car"}
    # dummy_translations = {"es": "un coche"}
    # dummy_summary = "A brief summary."
    #
    # # Call the function
    # # archive_analysis_artifacts(
    # #     BUCKET_NAME,
    # #     IMAGE_ID,
    # #     dummy_image_content,
    # #     dummy_analysis,
    # #     alt_text_translations=dummy_translations,
    # #     summary_text=dummy_summary
    # # )
    pass