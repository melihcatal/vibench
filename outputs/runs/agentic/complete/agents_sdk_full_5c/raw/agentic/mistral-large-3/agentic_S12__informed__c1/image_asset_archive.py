import os
import json
from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError


def archive_image_analysis(
    image_path: str,
    analysis_results: Dict[str, Any],
    bucket_name: str,
    object_key: str
) -> bool:
    """Archive image-analysis artifacts and derived captions in Amazon S3."""
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name="us-east-1"
    )

    # Upload image
    try:
        s3_client.upload_file(image_path, bucket_name, f"images/{object_key}")
    except ClientError:
        return False

    # Upload analysis results
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=f"analysis/{object_key}.json",
            Body=json.dumps(analysis_results, indent=2)
        )
    except ClientError:
        return False

    return True