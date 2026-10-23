import os
import json
from google.cloud import storage


def archive_image_analysis_artifacts(
    bucket_name: str,
    image_id: str,
    image_data: bytes,
    analysis_results: dict,
    caption_text: str,
) -> dict:
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Upload original image
    image_blob = bucket.blob(f"{image_id}/original_image.jpg")
    image_blob.upload_from_string(image_data, content_type="image/jpeg")

    # Upload analysis results as JSON
    analysis_json_blob = bucket.blob(f"{image_id}/analysis_results.json")
    analysis_json_blob.upload_from_string(
        json.dumps(analysis_results, indent=2), content_type="application/json"
    )

    # Upload caption text
    caption_blob = bucket.blob(f"{image_id}/caption.txt")
    caption_blob.upload_from_string(caption_text, content_type="text/plain")

    return {
        "image_uri": image_blob.public_url,
        "analysis_results_uri": analysis_json_blob.public_url,
        "caption_uri": caption_blob.public_url,
    }
