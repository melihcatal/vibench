import os
from google.cloud import storage
from google.api_core.exceptions import GoogleAPICallError

def archive_data_to_gcs(bucket_name: str, blob_name: str, data: bytes) -> str:
    """
    Archives exported document data into Google Cloud Storage.

    Requires GOOGLE_APPLICATION_CREDENTIALS to be set in the environment.

    :param bucket_name: The name of the GCS bucket.
    :param blob_name: The name for the new blob (file) in the bucket.
    :param data: The data (as bytes) to upload.
    :return: The public URL of the uploaded blob.
    """
    try:
        # The client automatically uses credentials from the environment.
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        blob.upload_from_string(data)

        print(f"Data successfully archived to gs://{bucket_name}/{blob_name}")
        return blob.public_url
        
    except GoogleAPICallError as e:
        print(f"Google Cloud Storage API error: {e}")
        raise
    except FileNotFoundError:
        print("Google Cloud credentials file not found. Set GOOGLE_APPLICATION_CREDENTIALS.")
        raise
