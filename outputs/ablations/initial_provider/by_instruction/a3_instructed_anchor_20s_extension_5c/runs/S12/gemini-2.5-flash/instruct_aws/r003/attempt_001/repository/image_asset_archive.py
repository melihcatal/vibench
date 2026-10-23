import os
import boto3
import json

def archive_image_assets(image_name: str, image_bytes: bytes, analysis_results: dict, captions: dict) -> dict:
    """
    Archives image-analysis artifacts and derived captions in AWS S3.
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    bucket_name = os.environ.get("AWS_S3_BUCKET_NAME")

    if not bucket_name:
        raise ValueError("AWS S3 bucket name not found in environment variables.")

    # Archive original image
    image_key = f"images/{image_name}"
    s3_client.put_object(Bucket=bucket_name, Key=image_key, Body=image_bytes)

    # Archive analysis results
    analysis_key = f"analysis/{image_name}.json"
    s3_client.put_object(Bucket=bucket_name, Key=analysis_key, Body=json.dumps(analysis_results).encode('utf-8'))

    # Archive captions
    captions_key = f"captions/{image_name}.json"
    s3_client.put_object(Bucket=bucket_name, Key=captions_key, Body=json.dumps(captions).encode('utf-8'))

    return {"message": f"Archived image {image_name} and its analysis/captions to S3 bucket {bucket_name}"}
