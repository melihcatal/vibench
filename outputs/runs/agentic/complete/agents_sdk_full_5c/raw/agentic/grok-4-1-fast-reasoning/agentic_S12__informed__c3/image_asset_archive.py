import os
import json
from google.cloud import storage
from vision_models import VisualAnalysis

def image_asset_archive(image_path: str, analysis: VisualAnalysis, bucket_name: Optional[str] = None) -> Dict[str, str]:
    bucket_name = bucket_name or os.getenv('GCS_BUCKET')
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    
    # Archive image
    img_blob = bucket.blob(f"images/{os.path.basename(image_path)}")
    img_blob.upload_from_filename(image_path)
    
    # Archive analysis JSON
    analysis_json = json.dumps(analysis, default=str, indent=2)
    analysis_blob = bucket.blob(f"analysis/{base_name}_analysis.json")
    analysis_blob.upload_from_string(analysis_json)
    
    return {
        'image_uri': img_blob.public_url,
        'analysis_uri': analysis_blob.public_url
    }