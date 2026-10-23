"""Archive image-analysis artifacts and derived captions in Amazon S3 managed object storage.

Provider: Amazon S3
SDK: boto3
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import datetime
import json
import os
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError


def create_s3_client(
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
) -> boto3.client:
    """Create and return a configured Amazon S3 boto3 client.

    Args:
        aws_access_key_id: AWS access key. Falls back to AWS_ACCESS_KEY_ID env var.
        aws_secret_access_key: AWS secret key. Falls back to AWS_SECRET_ACCESS_KEY env var.
        region: AWS region. Falls back to AWS_DEFAULT_REGION env var.

    Returns:
        A boto3 S3 client instance.
    """
    kwargs: Dict[str, Any] = {}
    if aws_access_key_id:
        kwargs["aws_access_key_id"] = aws_access_key_id
    if aws_secret_access_key:
        kwargs["aws_secret_access_key"] = aws_secret_access_key
    if region:
        kwargs["region_name"] = region

    session = boto3.Session(**kwargs)
    return session.client("s3")


def ensure_bucket_exists(
    s3_client: boto3.client,
    bucket_name: str,
    region: str = "us-east-1",
) -> bool:
    """Ensure the specified S3 bucket exists; create it if it does not.

    Args:
        s3_client: A boto3 S3 client.
        bucket_name: The S3 bucket name.
        region: AWS region for bucket creation.

    Returns:
        True if the bucket exists or was created successfully.
    """
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        return True
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "404":
            if region == "us-east-1":
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={"LocationConstraint": region},
                )
            return True
        raise


def upload_analysis_json(
    s3_client: boto3.client,
    bucket_name: str,
    analysis_data: Dict[str, Any],
    image_name: str,
    prefix: str = "image-analysis",
) -> str:
    """Upload image analysis results as a JSON object to S3.

    Args:
        s3_client: A boto3 S3 client.
        bucket_name: The S3 bucket name.
        analysis_data: Dict containing the analysis results.
        image_name: Original image filename (used for object key).
        prefix: S3 key prefix.

    Returns:
        The S3 object key of the uploaded artifact.
    """
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    safe_name = image_name.rsplit(".", 1)[0] if "." in image_name else image_name
    object_key = f"{prefix}/{safe_name}/{timestamp}/analysis.json"

    s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=json.dumps(analysis_data, indent=2, default=str).encode("utf-8"),
        ContentType="application/json",
    )
    return object_key


def upload_image_file(
    s3_client: boto3.client,
    bucket_name: str,
    image_path: str,
    prefix: str = "image-analysis",
) -> str:
    """Upload the original image file to S3.

    Args:
        s3_client: A boto3 S3 client.
        bucket_name: The S3 bucket name.
        image_path: Local path to the image file.
        prefix: S3 key prefix.

    Returns:
        The S3 object key of the uploaded image.
    """
    image_name = os.path.basename(image_path)
    object_key = f"{prefix}/{image_name}"

    s3_client.upload_file(
        Filename=image_path,
        Bucket=bucket_name,
        Key=object_key,
    )
    return object_key


def upload_derived_caption(
    s3_client: boto3.client,
    bucket_name: str,
    caption_text: str,
    image_name: str,
    prefix: str = "image-analysis",
) -> str:
    """Upload a derived caption / alt text to S3.

    Args:
        s3_client: A boto3 S3 client.
        bucket_name: The S3 bucket name.
        caption_text: The caption or alt text content.
        image_name: Original image filename (used for object key).
        prefix: S3 key prefix.

    Returns:
        The S3 object key of the uploaded caption.
    """
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    safe_name = image_name.rsplit(".", 1)[0] if "." in image_name else image_name
    object_key = f"{prefix}/{safe_name}/{timestamp}/caption.txt"

    s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=caption_text.encode("utf-8"),
        ContentType="text/plain",
    )
    return object_key


def archive_image_analysis(
    image_path: str,
    analysis_results: Dict[str, Any],
    caption_text: Optional[str] = None,
    bucket_name: Optional[str] = None,
    prefix: str = "image-analysis",
    region: str = "us-east-1",
) -> dict:
    """Archive an image, its analysis results, and derived caption to Amazon S3.

    Args:
        image_path: Local path to the image file.
        analysis_results: Dict of all analysis results to archive.
        caption_text: Optional derived caption or summary text.
        bucket_name: S3 bucket name. Falls back to S3_BUCKET_NAME env var.
        prefix: S3 key prefix.
        region: AWS region.

    Returns:
        A dict with uploaded S3 keys and provider metadata.
    """
    bucket = bucket_name or os.environ.get("S3_BUCKET_NAME", "image-analysis-archive")

    s3_client = create_s3_client(region=region)
    ensure_bucket_exists(s3_client, bucket, region=region)

    image_key = upload_image_file(s3_client, bucket, image_path, prefix=prefix)
    analysis_key = upload_analysis_json(
        s3_client, bucket, analysis_results, os.path.basename(image_path), prefix=prefix
    )

    caption_key = None
    if caption_text:
        caption_key = upload_derived_caption(
            s3_client, bucket, caption_text, os.path.basename(image_path), prefix=prefix
        )

    return {
        "provider": "amazon-s3",
        "bucket": bucket,
        "image_key": image_key,
        "analysis_key": analysis_key,
        "caption_key": caption_key,
    }


if __name__ == "__main__":
    sample_image = os.environ.get("VISION_IMAGE_PATH", "sample.jpg")
    sample_analysis = {
        "labels": [{"name": "cat", "confidence": 0.95}],
        "description": {"text": "a cat on a windowsill", "confidence": 0.89},
    }
    sample_caption = "A domestic cat sitting peacefully on a windowsill, looking outside."

    result = archive_image_analysis(
        image_path=sample_image,
        analysis_results=sample_analysis,
        caption_text=sample_caption,
    )
    print(result)
