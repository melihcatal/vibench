import os
import json
from typing import Dict, Any
from google.cloud import storage

def image_asset_archive(image_path: str, analysis_results: Dict[str, Any], bucket_name: str, prefix: str = 'vision-analysis/') -> Dict[str, str]:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    
    image_name = os.path.basename(image_path)
    image_blob_name = f"{prefix}{image_name}"
    bucket.blob(image_blob_name).upload_from_filename(image_path)
    
    results_name = f"{prefix}results_{os.path.splitext(image_name)[0]}.json"
    bucket.blob(results_name).upload_from_string(json.dumps(analysis_results, indent=2))
    
    return {
        'image_key': image_blob_name,
        'results_key': results_name
    }