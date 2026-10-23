import os
import json
import base64
from google.cloud import storage
from vision_models import ImageAnalysisResults, ImageData

def archive_image_analysis_artifacts(
    image_data: ImageData,
    analysis_results: ImageAnalysisResults,
    bucket_name: str,
    base_object_name: str, # e.g., 'my-image-123'
) -> str:
    """
    Archives image-analysis artifacts and derived captions in Google Cloud Storage.
    Stores the original image (if provided as content) and a JSON file with analysis metadata.
    Returns the GCS URI of the analysis results JSON file.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    original_image_gcs_uri = None
    if image_data.content:
        image_bytes = base64.b64decode(image_data.content)
        image_blob = bucket.blob(f"{base_object_name}/original_image.jpg")
        image_blob.upload_from_string(image_bytes, content_type="image/jpeg")
        original_image_gcs_uri = image_blob.public_url
    elif image_data.gcs_uri:
        original_image_gcs_uri = image_data.gcs_uri

    results_dict = {
        "image_source": {
            "original_content_archived_uri": original_image_gcs_uri,
            "input_gcs_uri_if_any": image_data.gcs_uri,
        },
        "labels": [l.__dict__ for l in analysis_results.labels] if analysis_results.labels else None,
        "description": analysis_results.description.__dict__ if analysis_results.description else None,
        "text": [t.__dict__ for t in analysis_results.text] if analysis_results.text else None,
        "safety_scores": analysis_results.safety_scores.__dict__ if analysis_results.safety_scores else None,
        "translated_description": analysis_results.translated_description,
        "moderation_flags": analysis_results.moderation_flags,
        "summary": analysis_results.summary,
    }

    metadata_blob_name = f"{base_object_name}/analysis_results.json"
    metadata_blob = bucket.blob(metadata_blob_name)
    metadata_blob.upload_from_string(
        json.dumps(results_dict, indent=2),
        content_type="application/json"
    )

    return metadata_blob.public_url
