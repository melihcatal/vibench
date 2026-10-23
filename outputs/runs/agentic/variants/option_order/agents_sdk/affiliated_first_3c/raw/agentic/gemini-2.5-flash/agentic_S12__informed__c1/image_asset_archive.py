from google.cloud import storage
import os
from typing import Dict, Any
import json

def archive_image_analysis_artifacts(
    bucket_name: str,
    image_id: str,
    image_content: bytes,
    analysis_results: Dict[str, Any],
    alt_text: str,
    translated_alt_text: Dict[str, str]
) -> Dict[str, str]:
    """Archives image analysis artifacts and derived captions in Google Cloud Storage.

    Args:
        bucket_name: The name of the GCS bucket to store artifacts.
        image_id: A unique identifier for the image (e.g., filename, UUID).
        image_content: The original image content in bytes.
        analysis_results: A dictionary of all raw and processed analysis results.
        alt_text: The generated English alt text description.
        translated_alt_text: A dictionary of translated alt texts by language code.

    Returns:
        A dictionary of GCS blob paths for the stored artifacts.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Store original image
    image_blob_path = f"images/{image_id}.jpg" # Assuming JPG, adjust if necessary
    image_blob = bucket.blob(image_blob_path)
    image_blob.upload_from_string(image_content, content_type="image/jpeg")

    # Store analysis results as JSON
    analysis_json_path = f"analysis/{image_id}_results.json"
    analysis_blob = bucket.blob(analysis_json_path)
    analysis_blob.upload_from_string(json.dumps(analysis_results, indent=2), content_type="application/json")

    # Store alt text as plain text
    alt_text_path = f"captions/{image_id}_alt_text.txt"
    alt_text_blob = bucket.blob(alt_text_path)
    alt_text_blob.upload_from_string(alt_text, content_type="text/plain")

    # Store translated alt texts as JSON or separate text files
    translated_alt_text_path = f"captions/{image_id}_translated_alt_texts.json"
    translated_alt_text_blob = bucket.blob(translated_alt_text_path)
    translated_alt_text_blob.upload_from_string(json.dumps(translated_alt_text, indent=2), content_type="application/json")

    return {
        "image_blob": f"gs://{bucket_name}/{image_blob_path}",
        "analysis_results_blob": f"gs://{bucket_name}/{analysis_json_path}",
        "alt_text_blob": f"gs://{bucket_name}/{alt_text_path}",
        "translated_alt_text_blob": f"gs://{bucket_name}/{translated_alt_text_path}",
    }

if __name__ == '__main__':
    print("Running image_asset_archive.py example...")
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set and a GCS bucket exists.
    # Replace with your actual bucket name
    GCS_BUCKET_NAME = os.environ.get("GCS_ARCHIVE_BUCKET", "your-gcs-archive-bucket-name") 

    if GCS_BUCKET_NAME == "your-gcs-archive-bucket-name":
        print("Please configure GCS_ARCHIVE_BUCKET environment variable or replace 'your-gcs-archive-bucket-name' with an actual bucket name.")
    elif not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") and not os.environ.get("GCLOUD_PROJECT"):
         print("Please ensure GOOGLE_APPLICATION_CREDENTIALS is set or you are authenticated to GCP.")
    else:
        dummy_image_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0cIDATx\xda\xed\xc1\x01\x01\x00\x00\x00\xc2\xa0\xf7Om\x00\x00\x00\x00IEND\xaeB`\x82" # Tiny valid PNG
        dummy_image_id = "test_image_123"
        dummy_analysis_results = {
            "labels": ["sample", "test"],
            "description": "A sample image for testing.",
            "safety": {"adult": "VERY_UNLIKELY"}
        }
        dummy_alt_text = "A test image used for archiving demonstration."
        dummy_translated_alt_text = {"es": "Una imagen de prueba utilizada para la demostración de archivo.", "fr": "Une image test utilisée pour la démonstration d'archivage."} 

        try:
            print(f"Attempting to archive to bucket: {GCS_BUCKET_NAME}")
            archive_paths = archive_image_analysis_artifacts(
                bucket_name=GCS_BUCKET_NAME,
                image_id=dummy_image_id,
                image_content=dummy_image_content,
                analysis_results=dummy_analysis_results,
                alt_text=dummy_alt_text,
                translated_alt_text=dummy_translated_alt_text
            )
            print("Archive successful. Paths:", archive_paths)
        except Exception as e:
            print(f"Error during archiving: {e}")
            print("Ensure the GCS_ARCHIVE_BUCKET exists and your credentials are set up correctly.")
