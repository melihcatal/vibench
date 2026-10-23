import os
from google.cloud import storage
from vision_models import ImageAnalysisResult


def archive_analysis_artifacts(
    analysis_result: ImageAnalysisResult, bucket_name: str, destination_blob_name: str
):
    storage_client = storage.Client()  # GOOGLE_APPLICATION_CREDENTIALS should be set
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # For demonstration, we'll create a simple text artifact summarizing the analysis
    artifact_content = f"Image URI: {analysis_result.image_uri}\n"
    if analysis_result.labels:
        artifact_content += f"Labels: {', '.join(analysis_result.labels)}\n"
    if analysis_result.description:
        artifact_content += f"Description: {analysis_result.description}\n"
    if analysis_result.text_annotations:
        detected_texts = [
            t["description"]
            for t in analysis_result.text_annotations
            if t["description"]
        ]
        if detected_texts:
            artifact_content += f"Detected Text: {', '.join(detected_texts)}\n"
    if analysis_result.safety_annotations:
        safety_info = ", ".join(
            [f"{k}: {v}" for k, v in analysis_result.safety_annotations.items()]
        )
        artifact_content += f"Safety: {safety_info}\n"

    blob.upload_from_string(artifact_content, content_type="text/plain")
    print(
        f"Artifact for {analysis_result.image_uri} uploaded to gs://{bucket_name}/{destination_blob_name}"
    )
