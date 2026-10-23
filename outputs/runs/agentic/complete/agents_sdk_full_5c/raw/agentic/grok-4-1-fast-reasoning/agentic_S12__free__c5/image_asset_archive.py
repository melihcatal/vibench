import os
import json
import boto3
from vision_client import get_s3_bucket

def image_asset_archive(image_path: str, analysis_artifacts: dict, bucket: str = None) -> dict:
    if bucket is None:
        bucket = get_s3_bucket()
    s3 = boto3.client("s3")
    image_name = os.path.basename(image_path)
    image_key = f"images/{image_name}"
    analysis_key = f"analysis/{os.path.splitext(image_name)[0]}_analysis.json"
    s3.upload_file(image_path, bucket, image_key)
    s3.put_object(
        Bucket=bucket,
        Key=analysis_key,
        Body=json.dumps(analysis_artifacts, indent=2).encode("utf-8")
    )
    return {"image_key": image_key, "analysis_key": analysis_key}