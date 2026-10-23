import os
import requests
from vision_client import VisionClient

def archive_image_asset(image_url: str, file_name: str, bucket_name: str) -> str | None:
    client_helper = VisionClient()
    gcs_client = client_helper.get_gcs_client()

    try:
        bucket = gcs_client.get_bucket(bucket_name)
        blob = bucket.blob(file_name)

        # Download the image from the URL
        response = requests.get(image_url)
        response.raise_for_status() # Raise an exception for HTTP errors
        image_data = response.content

        # Upload the image data to Google Cloud Storage
        blob.upload_from_string(image_data, content_type=response.headers['Content-Type'])

        # Optionally, store analysis results as metadata or separate files
        # For this task, we'll just archive the image asset itself.

        return blob.public_url # Google Cloud Storage Specific
    except Exception as e:
        print(f"Error archiving image asset: {e}")
        return None
