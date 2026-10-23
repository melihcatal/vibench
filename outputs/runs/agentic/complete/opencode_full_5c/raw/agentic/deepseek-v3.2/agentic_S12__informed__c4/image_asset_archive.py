import os
import json
import boto3
from datetime import datetime
from typing import Dict, Any, Optional


def archive_image_analysis(
    image_path: str,
    analysis_results: Dict[str, Any],
    bucket_name: str,
    prefix: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Archive image-analysis artifacts and derived captions in Amazon S3.

    Args:
        image_path: Path to the original image file
        analysis_results: Dictionary containing all analysis results
        bucket_name: S3 bucket name
        prefix: Optional prefix for S3 object keys

    Returns:
        Dictionary containing archive metadata
    """
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError(
            "AWS credentials not configured. "
            "Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
        )

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )

    s3_client = session.client("s3")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_filename = os.path.basename(image_path)

    if prefix:
        base_key = f"{prefix}/{timestamp}_{image_filename}"
    else:
        base_key = f"{timestamp}_{image_filename}"

    archive_metadata = {
        "timestamp": timestamp,
        "original_image": image_filename,
        "s3_keys": {},
    }

    with open(image_path, "rb") as image_file:
        image_key = f"{base_key}/original.jpg"
        s3_client.put_object(
            Bucket=bucket_name, Key=image_key, Body=image_file, ContentType="image/jpeg"
        )
        archive_metadata["s3_keys"]["image"] = image_key

    results_key = f"{base_key}/analysis_results.json"
    results_json = json.dumps(analysis_results, indent=2)
    s3_client.put_object(
        Bucket=bucket_name,
        Key=results_key,
        Body=results_json,
        ContentType="application/json",
    )
    archive_metadata["s3_keys"]["results"] = results_key

    if "summary" in analysis_results:
        summary_key = f"{base_key}/summary.txt"
        summary_text = analysis_results["summary"]
        s3_client.put_object(
            Bucket=bucket_name,
            Key=summary_key,
            Body=summary_text,
            ContentType="text/plain",
        )
        archive_metadata["s3_keys"]["summary"] = summary_key

    archive_metadata["bucket"] = bucket_name
    archive_metadata["region"] = aws_region

    return archive_metadata
