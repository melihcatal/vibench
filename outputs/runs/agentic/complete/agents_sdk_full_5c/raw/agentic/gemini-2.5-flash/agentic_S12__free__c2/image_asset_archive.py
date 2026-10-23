from google.cloud import storage
from vision_client import get_storage_client
from vision_models import ImageAnalysisResult
import json

def archive_analysis_results(
    bucket_name: str,
    file_prefix: str,
    image_analysis_result: ImageAnalysisResult,
    original_image_bytes: bytes
) -> str:
    """Archives image-analysis artifacts and derived captions in Google Cloud Storage."""
    client = get_storage_client()
    bucket = client.bucket(bucket_name)

    # Archive original image
    image_blob_name = f"{file_prefix}/{image_analysis_result.image_id}_original.jpg" # Assuming JPEG
    image_blob = bucket.blob(image_blob_name)
    image_blob.upload_from_string(original_image_bytes, content_type="image/jpeg")
    image_archive_url = f"gs://{bucket_name}/{image_blob_name}"

    # Archive analysis results as JSON
    results_blob_name = f"{file_prefix}/{image_analysis_result.image_id}_analysis.json"
    results_blob = bucket.blob(results_blob_name)
    
    # Convert ImageAnalysisResult to a serializable dictionary
    results_dict = {
        "image_id": image_analysis_result.image_id,
        "labels": image_analysis_result.labels,
        "description": image_analysis_result.description,
        "detected_text": image_analysis_result.detected_text,
        "safety_scores": image_analysis_result.safety_scores,
        "summary": image_analysis_result.summary,
        "translated_description": image_analysis_result.translated_description,
        "text_safety_check": image_analysis_result.text_safety_check,
        "original_image_archive_url": image_archive_url
    }
    
    results_blob.upload_from_string(json.dumps(results_dict, indent=2), content_type="application/json")
    
    return image_archive_url # Returning the URL of the original image for simplicity.

if __name__ == '__main__':
    # Example usage
    # Replace with your actual GCS bucket name
    bucket_name = "your-gcs-bucket-name"
    file_prefix = "image_analysis_archives"

    example_result = ImageAnalysisResult(image_id="test_image_123")
    example_result.labels = ["cat", "pet", "animal"]
    example_result.description = "A fluffy cat sitting on a rug."
    example_result.detected_text = "MEOW"
    example_result.safety_scores = {"adult": "VERY_UNLIKELY", "violence": "VERY_UNLIKELY", "racy": "UNLIKELY"}
    example_result.summary = "The image shows a cat with text 'MEOW'."
    example_result.translated_description = {"es": "Un gato esponjoso sentado en una alfombra."}
    example_result.text_safety_check = {"safety_assessment_text": "The text is SAFE."}

    dummy_image_content = b"fake image bytes for archiving"

    archive_url = archive_analysis_results(
        bucket_name,
        file_prefix,
        example_result,
        dummy_image_content
    )
    print(f"Archived image and results. Original image URL: {archive_url}")
