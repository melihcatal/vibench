from google.cloud import storage
import os
from vision_models import ImageAssetArchiveRequest, ImageAssetArchiveResponse
import json


def image_asset_archive(request: ImageAssetArchiveRequest) -> ImageAssetArchiveResponse:
    storage_client = storage.Client()
    # GOOGLE_APPLICATION_CREDENTIALS environment variable is expected

    bucket_name = os.environ.get("GCS_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME environment variable not set.")

    bucket = storage_client.bucket(bucket_name)

    # Create a unique filename for the archive artifact
    # Using the image_uri to derive a blob name, could be more robust with UUIDs
    image_id = request.image_uri.split("/")[-1].split(".")[0]
    blob_name = f"image_analysis_archive/{image_id}_analysis.json"

    blob = bucket.blob(blob_name)

    # Prepare the data to be archived
    archive_data = {
        "image_uri": request.image_uri,
        "labels": request.labels,
        "description": request.description,
        "summary": request.summary,
        "translated_text": request.translated_text,
        "safety_scores": request.safety_scores,
        "text_safety_scores": request.text_safety_scores,
    }

    # Upload the JSON data to Google Cloud Storage
    blob.upload_from_string(json.dumps(archive_data), content_type="application/json")

    return ImageAssetArchiveResponse(archive_url=blob.public_url)
