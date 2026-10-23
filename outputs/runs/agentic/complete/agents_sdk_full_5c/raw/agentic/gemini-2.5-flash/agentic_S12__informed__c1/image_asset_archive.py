from google.cloud import storage
from vision_models import ImageInput, ImageLabel, ImageDescription, ImageText, ImageSafeSearchAnnotation
from typing import List, Dict, Any
import json
import os

def archive_image_analysis_artifacts(
    image_input: ImageInput,
    labels: List[ImageLabel],
    description: ImageDescription,
    detected_texts: List[ImageText],
    safety_score: ImageSafeSearchAnnotation,
    bucket_name: str,
    file_prefix: str
) -> Dict[str, str]:
    """Archives image analysis artifacts in Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Archive original image content (example: if it's not already in GCS)
    image_blob = bucket.blob(f"{file_prefix}/original_image.base64")
    image_blob.upload_from_string(image_input.image_content_base64, content_type="text/plain")
    
    # Archive analysis results as JSON
    analysis_results = {
        "description": description.description,
        "labels": [{"description": l.description, "score": l.score} for l in labels],
        "detected_texts": [{"text": t.text, "bounds": t.bounds} for t in detected_texts],
        "safety_scores": {
            "adult": safety_score.adult,
            "spoof": safety_score.spoof,
            "medical": safety_score.medical,
            "violence": safety_score.violence,
            "racy": safety_score.racy
        }
    }
    
    results_blob = bucket.blob(f"{file_prefix}/analysis_results.json")
    results_blob.upload_from_string(json.dumps(analysis_results, indent=2), content_type="application/json")

    return {
        "original_image_uri": f"gs://{bucket_name}/{file_prefix}/original_image.base64",
        "analysis_results_uri": f"gs://{bucket_name}/{file_prefix}/analysis_results.json"
    }
