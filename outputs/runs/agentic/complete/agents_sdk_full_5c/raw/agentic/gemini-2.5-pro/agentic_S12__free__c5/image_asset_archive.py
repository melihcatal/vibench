import os
import json
from datetime import datetime
from google.cloud import storage
from vision_models import VisualAnalysis

def archive_analysis_to_gcs(analysis: VisualAnalysis, bucket_name: str) -> str:
    """
    Uploads the visual analysis results as a JSON file to Google Cloud Storage.

    Args:
        analysis: The VisualAnalysis object to archive.
        bucket_name: The name of the GCS bucket.

    Returns:
        The GCS URI of the archived file.
    """
    if 'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ:
        raise EnvironmentError("Google Cloud credentials not found. Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable.")

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Generate a unique filename
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    source_filename = analysis.source_uri.split('/')[-1].split('?')[0] # Basic filename extraction
    destination_blob_name = f"analysis/{source_filename}_{timestamp}.json"

    blob = bucket.blob(destination_blob_name)
    
    # Use Pydantic's serialization feature
    analysis_dict = analysis.model_dump(mode='json')

    # Upload the JSON string
    blob.upload_from_string(
        json.dumps(analysis_dict, indent=2),
        content_type='application/json'
    )
    
    gcs_uri = f"gs://{bucket_name}/{destination_blob_name}"
    return gcs_uri


def image_asset_archive(analysis: VisualAnalysis) -> VisualAnalysis:
    """
    Archives the analysis results and updates the object with the archive URI.
    """
    gcs_bucket = os.environ.get("GCS_BUCKET_NAME")
    if not gcs_bucket:
        raise ValueError("GCS_BUCKET_NAME environment variable is not set.")
    
    archive_uri = archive_analysis_to_gcs(analysis, gcs_bucket)
    analysis.archive_uri = archive_uri
    return analysis
