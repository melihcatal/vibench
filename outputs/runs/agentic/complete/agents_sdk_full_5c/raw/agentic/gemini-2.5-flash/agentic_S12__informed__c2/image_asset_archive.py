from google.cloud import storage
import os

def archive_asset(bucket_name: str, destination_blob_name: str, data_to_upload: bytes, content_type: str = "application/json") -> str:
    """Archives image-analysis artifacts and derived captions in Google Cloud Storage."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data_to_upload, content_type=content_type)

    return f"gs://{bucket_name}/{destination_blob_name}"

if __name__ == '__main__':
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # Replace with your actual bucket name
    my_bucket = os.environ.get("GCS_BUCKET_NAME", "your-gcs-bucket-name")

    # Example artifact: a JSON string of analysis results
    analysis_results = '''{"labels": ["tree", "sky"], "description": "A scene with trees."}
    '''
    artifact_data = analysis_results.encode('utf-8')
    blob_name = "image_analysis/my_image_analysis.json"

    uploaded_uri = archive_asset(my_bucket, blob_name, artifact_data)
    print(f"Archived analysis results to: {uploaded_uri}")

    # Example: archiving an image itself
    dummy_image_data = b"fake_image_binary_data"
    image_blob_name = "raw_images/my_image.jpg"
    uploaded_image_uri = archive_asset(my_bucket, image_blob_name, dummy_image_data, content_type="image/jpeg")
    print(f"Archived image to: {uploaded_image_uri}")
