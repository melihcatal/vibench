import os
import json
import boto3
from datetime import datetime
from typing import Dict, Any, Optional


def image_asset_archive(
    image_path: str,
    analysis_results: Dict[str, Any],
    bucket_name: str,
    prefix: Optional[str] = None,
) -> Dict[str, str]:
    """Archive image-analysis artifacts and derived captions in AWS S3."""
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    image_filename = os.path.basename(image_path)

    if prefix:
        base_prefix = f"{prefix.rstrip('/')}/{timestamp}"
    else:
        base_prefix = f"image-analysis/{timestamp}"

    # Upload original image
    with open(image_path, "rb") as image_file:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=f"{base_prefix}/original/{image_filename}",
            Body=image_file,
            ContentType="image/jpeg",
        )

    # Upload analysis results as JSON
    analysis_json = json.dumps(analysis_results, indent=2)
    s3_client.put_object(
        Bucket=bucket_name,
        Key=f"{base_prefix}/analysis/results.json",
        Body=analysis_json,
        ContentType="application/json",
    )

    # Extract and upload description as separate text file
    if "description" in analysis_results:
        description = analysis_results.get("description", {}).get("description", "")
        if description:
            s3_client.put_object(
                Bucket=bucket_name,
                Key=f"{base_prefix}/captions/description.txt",
                Body=description,
                ContentType="text/plain",
            )

    # Generate and upload a summary metadata file
    metadata = {
        "timestamp": timestamp,
        "original_image": image_filename,
        "analysis_files": [
            f"{base_prefix}/original/{image_filename}",
            f"{base_prefix}/analysis/results.json",
        ],
        "bucket": bucket_name,
    }

    if "description" in analysis_results:
        metadata["analysis_files"].append(f"{base_prefix}/captions/description.txt")

    metadata_json = json.dumps(metadata, indent=2)
    s3_client.put_object(
        Bucket=bucket_name,
        Key=f"{base_prefix}/metadata.json",
        Body=metadata_json,
        ContentType="application/json",
    )

    return {
        "image_url": f"s3://{bucket_name}/{base_prefix}/original/{image_filename}",
        "analysis_url": f"s3://{bucket_name}/{base_prefix}/analysis/results.json",
        "metadata_url": f"s3://{bucket_name}/{base_prefix}/metadata.json",
        "bucket": bucket_name,
        "prefix": base_prefix,
    }
