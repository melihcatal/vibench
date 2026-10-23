
import os
from google.cloud import storage

def archive_analysis_artifacts(
    bucket_name: str, 
    image_id: str, 
    image_bytes: bytes, 
    analysis_json: dict, 
    caption_text: str
) -> dict:
    """Archives image analysis artifacts and derived captions in Google Cloud Storage."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Archive original image
    image_blob = bucket.blob(f"{image_id}/original_image.jpg")
    image_blob.upload_from_string(image_bytes, content_type="image/jpeg")
    
    # Archive analysis JSON
    analysis_blob = bucket.blob(f"{image_id}/analysis_results.json")
    analysis_blob.upload_from_string(
        data=str(analysis_json),  # Convert dict to string for storage
        content_type="application/json"
    )

    # Archive caption text
    caption_blob = bucket.blob(f"{image_id}/caption.txt")
    caption_blob.upload_from_string(caption_text, content_type="text/plain")
    
    return {
        "image_url": image_blob.public_url,
        "analysis_url": analysis_blob.public_url,
        "caption_url": caption_blob.public_url
    }

if __name__ == '__main__':
    # This is example usage.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set and the bucket exists.
    # Replace with actual data for testing.
    example_bucket_name = os.environ.get("GCS_BUCKET_NAME")
    if not example_bucket_name:
        print("Please set GCS_BUCKET_NAME environment variable.")
    else:
        example_image_id = "test_image_123"
        example_image_bytes = b"fake_image_content"  # Replace with actual image bytes
        example_analysis_json = {"labels": ["test_label"], "description": "A test image."}
        example_caption_text = "This is a test caption for the image."

        try:
            archive_info = archive_analysis_artifacts(
                example_bucket_name,
                example_image_id,
                example_image_bytes,
                example_analysis_json,
                example_caption_text
            )
            print("Archiving successful:", archive_info)
        except Exception as e:
            print(f"An error occurred during archiving: {e}")
