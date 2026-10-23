import json
from google.cloud import storage
from vision_client import get_storage_client
from vision_models import VisualAnalysis


def archive_assets(
    analysis: VisualAnalysis,
    image_path: str,
    bucket_name: str,
    archive_prefix: str,
):
    storage_client = get_storage_client()
    bucket = storage_client.bucket(bucket_name)

    image_filename = image_path.split("/")[-1]

    # Archive original image
    image_blob = bucket.blob(f"{archive_prefix}/{image_filename}")
    image_blob.upload_from_filename(image_path)

    # Archive analysis results
    analysis_blob = bucket.blob(f"{archive_prefix}/{image_filename}.json")
    analysis_data = analysis.model_dump_json(indent=2)
    analysis_blob.upload_from_string(analysis_data, content_type="application/json")

    # Archive just the description as a text file
    if analysis.description:
        caption_blob = bucket.blob(f"{archive_prefix}/{image_filename}.txt")
        caption_blob.upload_from_string(
            analysis.description.text, content_type="text/plain"
        )
