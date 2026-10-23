import os
from google.cloud import storage
from typing import Dict, Any

def image_asset_archive(
    image_path: str,
    analysis_results: Dict[str, Any],
    bucket_name: str
) -> str:
    """Archives image-analysis artifacts and derived captions in Google Cloud Storage."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    
    # Upload the original image
    image_blob = bucket.blob(f"images/{os.path.basename(image_path)}")
    image_blob.upload_from_filename(image_path)
    
    # Upload the analysis results
    results_blob = bucket.blob(f"analysis/{os.path.basename(image_path)}.json")
    results_blob.upload_from_string(str(analysis_results))
    
    return f"gs://{bucket_name}/analysis/{os.path.basename(image_path)}.json"