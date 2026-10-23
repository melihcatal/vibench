import os
import json
import boto3
from datetime import datetime
from typing import Dict, Any, Optional


def archive_image_analysis(
    image_path: str, analysis_results: Dict[str, Any], bucket_name: Optional[str] = None
) -> Dict[str, Any]:
    """Archive image-analysis artifacts and derived captions in AWS S3."""

    if not bucket_name:
        bucket_name = os.getenv("AWS_S3_BUCKET")
        if not bucket_name:
            raise ValueError("AWS_S3_BUCKET environment variable not set")

    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError("AWS credentials environment variables not set")

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_filename = os.path.basename(image_path)
    base_name = os.path.splitext(image_filename)[0]

    archive_data = {
        "timestamp": timestamp,
        "image_filename": image_filename,
        "analysis_results": analysis_results,
        "archive_date": datetime.now().isoformat(),
    }

    json_data = json.dumps(archive_data, indent=2)

    json_key = f"analysis/{base_name}_{timestamp}.json"

    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        image_key = (
            f"images/{base_name}_{timestamp}{os.path.splitext(image_filename)[1]}"
        )

        s3_client.put_object(
            Bucket=bucket_name,
            Key=json_key,
            Body=json_data.encode("utf-8"),
            ContentType="application/json",
        )

        s3_client.put_object(
            Bucket=bucket_name, Key=image_key, Body=image_data, ContentType="image/jpeg"
        )

        return {
            "success": True,
            "json_key": json_key,
            "image_key": image_key,
            "bucket": bucket_name,
            "timestamp": timestamp,
        }

    except Exception as e:
        return {"success": False, "error": str(e), "timestamp": timestamp}
