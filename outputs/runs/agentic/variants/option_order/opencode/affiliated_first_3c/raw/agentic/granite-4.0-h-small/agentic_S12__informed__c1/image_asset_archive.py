# Archive image-analysis artifacts and derived captions in managed object storage
import os
import boto3
from vision_client import get_s3_client


def image_asset_archive(image_path: str, analysis_data: dict):
    """Archive image file and its analysis results (labels, description, text) to S3."""
    s3 = get_s3_client()
    bucket = os.getenv("AWS_S3_BUCKET")
    # Generate a deterministic key based on image filename
    key = os.path.basename(image_path)
    # Store the original image
    s3.upload_file(image_path, bucket, key)
    # Store analysis JSON
    analysis_key = f"{os.path.splitext(key)[0]}.json"
    s3.put_object(Bucket=bucket, Key=analysis_key, Body=json.dumps(analysis_data))
    return f"s3://{bucket}/{key}"
