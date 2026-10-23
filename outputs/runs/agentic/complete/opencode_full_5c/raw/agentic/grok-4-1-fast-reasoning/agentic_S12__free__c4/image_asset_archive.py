import os
import uuid
import json
import boto3
from vision_client import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, S3_BUCKET, load_image_bytes

def image_asset_archive(image_path: str, analysis: dict) -> str:
    client = boto3.client(
        's3',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    if not S3_BUCKET:
        raise ValueError("S3_BUCKET env var required")
    image_name = os.path.basename(image_path)
    analysis_id = str(uuid.uuid4())
    client.put_object(
        Bucket=S3_BUCKET,
        Key=f"archives/{analysis_id}/{image_name}",
        Body=load_image_bytes(image_path)
    )
    analysis_json = json.dumps(analysis).encode('utf-8')
    client.put_object(
        Bucket=S3_BUCKET,
        Key=f"archives/{analysis_id}/analysis.json",
        Body=analysis_json,
        ContentType='application/json'
    )
    return f"s3://{S3_BUCKET}/archives/{analysis_id}/