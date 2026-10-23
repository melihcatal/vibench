import os
from google.cloud import storage

def archive_image_analysis_artifacts(
    bucket_name: str,
    original_image_bytes: bytes,
    analysis_results_json: str, # JSON string of analysis results
    image_filename: str,
    results_filename: str,
) -> tuple[str, str]:
    """
    Archives original image and its analysis results to Google Cloud Storage.
    Returns the public URLs of the uploaded files.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Upload original image
    image_blob = bucket.blob(f"images/{image_filename}")
    image_blob.upload_from_string(original_image_bytes, content_type="image/jpeg") # Assuming JPEG
    image_url = image_blob.public_url

    # Upload analysis results JSON
    results_blob = bucket.blob(f"analysis_results/{results_filename}")
    results_blob.upload_from_string(analysis_results_json, content_type="application/json")
    results_url = results_blob.public_url

    return image_url, results_url

if __name__ == '__main__':
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # and GOOGLE_CLOUD_PROJECT_ID is set (implicitly used by storage client)
    # And you have a bucket created in your GCP project.
    
    BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME")
    if not BUCKET_NAME:
        print("Please set the GCS_BUCKET_NAME environment variable.")
    else:
        dummy_image_data = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0cIDATx\xda\xed\xc1\x01\x01\x00\x00\x00\xc2\xa0\xf7Om\x00\x00\x00\x00IEND\xaeB`\x82"
        dummy_results_json = '''{"labels": ["dummy"], "description": "A dummy image."}'''
        
        try:
            image_url, results_url = archive_image_analysis_artifacts(
                bucket_name=BUCKET_NAME,
                original_image_bytes=dummy_image_data,
                analysis_results_json=dummy_results_json,
                image_filename="test_image.png",
                results_filename="test_analysis_results.json"
            )
            print(f"Archived image URL: {image_url}")
            print(f"Archived results URL: {results_url}")
        except Exception as e:
            print(f"Error archiving assets to GCS: {e}")
            print("Please ensure your GCS_BUCKET_NAME environment variable is correct and that your service account has appropriate permissions.")
