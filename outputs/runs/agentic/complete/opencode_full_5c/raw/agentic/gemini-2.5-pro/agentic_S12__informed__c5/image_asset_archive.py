import json
from google.cloud import storage
from vision_models import VisualAnalysis


def image_asset_archive(
    bucket_name: str, blob_name: str, analysis_data: VisualAnalysis
):
    """Uploads visual analysis data to a Google Cloud Storage bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Serialize the Pydantic model to a JSON string
    json_data = analysis_data.model_dump_json(indent=2)

    blob.upload_from_string(json_data, content_type="application/json")

    print(f"File {blob_name} uploaded to {bucket_name}.")
