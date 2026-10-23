import os
import json
from typing import Dict, Any
import boto3
from datetime import datetime
from vision_client import get_aws_credentials


def archive_image_analysis(
    image_path: str, analysis_results: Dict[str, Any], bucket_name: str = None
) -> Dict[str, Any]:
    """
    Archive image-analysis artifacts and derived captions in AWS S3.

    Args:
        image_path: Path to the original image file
        analysis_results: Dictionary containing analysis results
        bucket_name: S3 bucket name (optional, uses env var if not provided)

    Returns:
        Dictionary containing archive metadata and URLs
    """
    if bucket_name is None:
        bucket_name = os.getenv("AWS_S3_BUCKET")
        if not bucket_name:
            raise ValueError("AWS_S3_BUCKET environment variable not set")

    aws_access_key, aws_secret_key, region = get_aws_credentials()

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region,
    )

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    image_filename = os.path.basename(image_path)
    base_name = os.path.splitext(image_filename)[0]

    archive_key = f"image-analysis/{base_name}_{timestamp}"

    with open(image_path, "rb") as image_file:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=f"{archive_key}/original/{image_filename}",
            Body=image_file,
            ContentType="image/jpeg",
        )

    analysis_json = json.dumps(analysis_results, indent=2)
    s3_client.put_object(
        Bucket=bucket_name,
        Key=f"{archive_key}/analysis/results.json",
        Body=analysis_json.encode("utf-8"),
        ContentType="application/json",
    )

    if "description" in analysis_results:
        description_text = analysis_results.get("description", {}).get("text", "")
        if description_text:
            s3_client.put_object(
                Bucket=bucket_name,
                Key=f"{archive_key}/captions/description.txt",
                Body=description_text.encode("utf-8"),
                ContentType="text/plain",
            )

    if "summary" in analysis_results:
        summary_text = analysis_results.get("summary", {}).get("summary", "")
        if summary_text:
            s3_client.put_object(
                Bucket=bucket_name,
                Key=f"{archive_key}/captions/summary.txt",
                Body=summary_text.encode("utf-8"),
                ContentType="text/plain",
            )

    bucket_location = s3_client.get_bucket_location(Bucket=bucket_name)
    region_name = bucket_location.get("LocationConstraint", "us-east-1")

    if region_name is None or region_name == "":
        region_name = "us-east-1"

    s3_base_url = f"https://{bucket_name}.s3.{region_name}.amazonaws.com"

    return {
        "archive_id": archive_key,
        "bucket": bucket_name,
        "region": region_name,
        "timestamp": timestamp,
        "artifacts": {
            "original_image": f"{s3_base_url}/{archive_key}/original/{image_filename}",
            "analysis_results": f"{s3_base_url}/{archive_key}/analysis/results.json",
            "description_caption": f"{s3_base_url}/{archive_key}/captions/description.txt"
            if "description" in analysis_results
            else None,
            "summary_caption": f"{s3_base_url}/{archive_key}/captions/summary.txt"
            if "summary" in analysis_results
            else None,
        },
        "provider": "aws-s3",
    }
