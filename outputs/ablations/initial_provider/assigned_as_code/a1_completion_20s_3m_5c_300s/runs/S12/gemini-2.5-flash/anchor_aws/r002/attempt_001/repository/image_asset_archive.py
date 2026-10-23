import boto3
import json
from typing import Dict, Any
from vision_client import get_s3_client
from vision_models import ArchiveAssetRequest, ArchiveAssetResponse

def image_asset_archive(payload: ArchiveAssetRequest, config: Dict[str, Any]) -> ArchiveAssetResponse:
    client = get_s3_client(config)
    bucket_name = config.get("s3_bucket_name")
    if not bucket_name:
        raise ValueError("S3 bucket name must be provided in config.")

    image_name = payload.image_name
    image_bytes = payload.image_bytes
    analysis_results = payload.analysis_results
    caption = payload.caption

    # Upload original image
    image_object_key = f"images/{image_name}"
    client.put_object(
        Bucket=bucket_name,
        Key=image_object_key,
        Body=image_bytes,
        ContentType='image/jpeg' # Assuming JPEG, can be made dynamic
    )
    image_url = f"https://{bucket_name}.s3.{config.get("region")}.amazonaws.com/{image_object_key}"

    # Upload analysis results as JSON
    analysis_object_key = f"analysis/{image_name.split('.')[0]}.json"
    client.put_object(
        Bucket=bucket_name,
        Key=analysis_object_key,
        Body=json.dumps(analysis_results, indent=2),
        ContentType='application/json'
    )
    # analysis_url = f"https://{bucket_name}.s3.{config.get("region")}.amazonaws.com/{analysis_object_key}"

    # Upload caption as a text file
    caption_object_key = f"captions/{image_name.split('.')[0]}.txt"
    client.put_object(
        Bucket=bucket_name,
        Key=caption_object_key,
        Body=caption.encode('utf-8'),
        ContentType='text/plain'
    )
    # caption_url = f"https://{bucket_name}.s3.{config.get("region")}.amazonaws.com/{caption_object_key}"

    return ArchiveAssetResponse(archive_url=image_url)
