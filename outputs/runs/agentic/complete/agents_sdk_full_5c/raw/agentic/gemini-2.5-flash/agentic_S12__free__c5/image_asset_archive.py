import os
from typing import Dict, Any
from vision_client import get_storage_client
import json

def archive_image_analysis_artifacts(
    bucket_name: str,
    destination_blob_prefix: str,
    image_uri: str,
    analysis_results: Dict[str, Any],
    caption: str = None,
    original_image_bytes: bytes = None,
):
    """Archives image analysis artifacts and derived captions in Google Cloud Storage."""
    client = get_storage_client()
    bucket = client.bucket(bucket_name)

    # Upload original image if provided
    if original_image_bytes:
        image_filename = os.path.basename(image_uri) if image_uri else "original_image.jpg"
        image_blob_name = f"{destination_blob_prefix}/{image_filename}"
        image_blob = bucket.blob(image_blob_name)
        image_blob.upload_from_string(original_image_bytes, content_type="image/jpeg") # Assuming JPEG, adjust as needed
        print(f"Uploaded original image to {image_blob.public_url}")

    # Upload analysis results as JSON
    results_filename = f"{destination_blob_prefix}/analysis_results.json"
    results_blob = bucket.blob(results_filename)
    results_blob.upload_from_string(json.dumps(analysis_results, indent=2), content_type="application/json")
    print(f"Uploaded analysis results to {results_blob.public_url}")

    # Upload caption if provided
    if caption:
        caption_filename = f"{destination_blob_prefix}/caption.txt"
        caption_blob = bucket.blob(caption_filename)
        caption_blob.upload_from_string(caption, content_type="text/plain")
        print(f"Uploaded caption to {caption_blob.public_url}")

    return True

if __name__ == '__main__':
    # This is a placeholder for demonstration.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set.
    # bucket = "your-gcs-bucket-name"
    # prefix = "image-analysis-artifacts/test-image-123"
    # example_results = {
    #     "labels": ["cat", "pet"],
    #     "description": "A domestic cat."
    # }
    # # archive_image_analysis_artifacts(
    # #     bucket_name=bucket,
    # #     destination_blob_prefix=prefix,
    # #     image_uri="gs://some-public-bucket/cat.jpg",
    # #     analysis_results=example_results,
    # #     caption="A small, furry cat with green eyes."
    # # )
    # print("Archiving process simulated.")
    pass
