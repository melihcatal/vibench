import os
from google.cloud import storage

def archive_analysis_artifact(bucket_name: str, destination_blob_name: str, data: str):
    """Archives image-analysis artifacts and derived captions in Google Cloud Storage.

    Args:
        bucket_name: The ID of your GCS bucket.
        destination_blob_name: The ID of your GCS object.
        data: The content to upload as a string.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data)

    print(f"File {destination_blob_name} uploaded to {bucket_name}.")

if __name__ == '__main__':
    # Example usage (replace with your bucket name and desired blob name)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    
    # WARNING: This will attempt to upload to your Google Cloud Storage bucket.
    # Make sure you have the necessary permissions and a valid bucket_name.

    # bucket_name = "your-gcs-bucket-name"
    # destination_blob_name = "image_analysis_report.json"
    # example_data = "{\"image_uri\": \"gs://...\", \"summary\": \"...\"}"

    # print(f"Archiving data to {destination_blob_name} in {bucket_name}:")
    # try:
    #     archive_analysis_artifact(bucket_name, destination_blob_name, example_data)
    # except Exception as e:
    #     print(f"Error archiving artifact: {e}")
    print("To run the example, uncomment the example usage block and replace placeholder values.")
