import os
import boto3
import json


def archive_image_analysis_artifacts(
    image_id: str, image_bytes: bytes, analysis_results: dict, bucket_name: str
) -> str:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    # Archive original image
    image_key = f"images/{image_id}.jpg"  # Assuming JPEG for simplicity
    s3_client.put_object(Bucket=bucket_name, Key=image_key, Body=image_bytes)

    # Archive analysis results as JSON
    analysis_key = f"analysis/{image_id}.json"
    s3_client.put_object(
        Bucket=bucket_name, Key=analysis_key, Body=json.dumps(analysis_results)
    )

    return f"Archived image and analysis results for {image_id} in S3 bucket {bucket_name}."
