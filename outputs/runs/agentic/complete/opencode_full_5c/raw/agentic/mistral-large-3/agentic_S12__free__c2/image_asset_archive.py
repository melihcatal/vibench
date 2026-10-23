import os
import boto3
from typing import Dict
from botocore.exceptions import ClientError


def archive_image_analysis_artifacts(
    image_path: str,
    analysis_results: Dict,
    bucket_name: str = "image-analysis-archive-bucket",
) -> str:
    """Archive image-analysis artifacts and derived captions in AWS S3."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    s3_client = boto3.client(
        "s3",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    image_key = f"images/{os.path.basename(image_path)}"
    results_key = f"results/{os.path.basename(image_path)}.json"

    try:
        # Upload image
        s3_client.upload_file(image_path, bucket_name, image_key)

        # Upload analysis results
        s3_client.put_object(
            Bucket=bucket_name, Key=results_key, Body=str(analysis_results)
        )

        return f"s3://{bucket_name}/{results_key}"
    except ClientError as e:
        raise Exception(f"Failed to archive artifacts: {e}")
