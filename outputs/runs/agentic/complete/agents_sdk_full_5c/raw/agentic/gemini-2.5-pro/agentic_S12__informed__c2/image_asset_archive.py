import json
from google.cloud import storage
from vision_models import FullImageAnalysis

def archive_results(bucket_name: str, destination_blob_name: str, data: FullImageAnalysis):
    """
    Uploads the image analysis results to a Google Cloud Storage bucket.

    Args:
        bucket_name: The name of the GCS bucket.
        destination_blob_name: The desired name for the object in the bucket.
        data: The FullImageAnalysis object to archive.
    """
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
    storage_client = storage.Client()
    
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Convert the Pydantic model to a JSON string
    json_data = data.model_dump_json(indent=2)

    blob.upload_from_string(json_data, content_type='application/json')

    print(
        f"Analysis results for {destination_blob_name} uploaded to gs://{bucket_name}/{destination_blob_name}."
    )
