# image_asset_archive.py
import os
from google.cloud import storage
from vision_models import ImageLabelsResponse, ImageDescriptionResponse, ImageTextDetectionResponse, SafetyCheckResponse
from image_summary import summarize_visual_analysis

def archive_image_results(image_path: str, analysis_labels: ImageLabelsResponse,
                          analysis_description: ImageDescriptionResponse,
                          analysis_text: ImageTextDetectionResponse,
                          analysis_safety: SafetyCheckResponse) -> str:
    # Summarize the results for naming
    summary = summarize_visual_analysis(analysis_labels, analysis_description, analysis_safety)
    filename = os.path.basename(image_path)
    prefix = 'vision-results'
    bucket_name = os.getenv('GCP_STORAGE_BUCKET')
    if not bucket_name:
        raise RuntimeError('Set GCP_STORAGE_BUCKET environment variable')
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob_name = f'{prefix}/{filename}.json'
    blob = bucket.blob(blob_name)
    results = {
        'image_path': image_path,
        'summary': summary,
        'ocr_text': [t['text'] for t in analysis_text.texts],
        'safety_raw': analysis_safety.safety_results
    }
    blob.upload_from_string(data=str(results), content_type='application/json')
    # Returns public URL (if bucket is public) or just the blob name
    blob.make_public()
    return blob.public_url
