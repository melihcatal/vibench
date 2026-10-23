import os
import json
import time
import boto3
from .vision_models import VisionResult

def image_asset_archive(image_path: str, analysis: VisionResult, bucket: str = None) -> str:
    bucket_name = bucket or os.getenv('S3_IMAGE_ARCHIVE_BUCKET')
    s3_client = boto3.client('s3')
    timestamp = int(time.time())
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    key = f'images/{base_name}_{timestamp}.json'
    artifacts = {
        'image_path': image_path,
        'analysis': analysis,
        'archived_at': timestamp
    }
    s3_client.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=json.dumps(artifacts, indent=2),
        ContentType='application/json'
    )
    return key