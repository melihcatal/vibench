import os
import json
import boto3
from botocore.exceptions import ClientError
from datetime import datetime


def archive_image_analysis(
    image_path, analysis_results, bucket_name, prefix="image-analysis"
):
    """Archive image-analysis artifacts and derived captions in Amazon S3."""
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required"
        )

    s3_client = boto3.client(
        "s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_filename = os.path.basename(image_path)
    base_name = os.path.splitext(image_filename)[0]

    archive_data = {
        "timestamp": timestamp,
        "image_filename": image_filename,
        "analysis_results": analysis_results,
        "metadata": {
            "archived_at": datetime.now().isoformat(),
            "provider": "Amazon S3",
        },
    }

    json_key = f"{prefix}/{base_name}_{timestamp}/analysis.json"

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=json_key,
            Body=json.dumps(archive_data, indent=2),
            ContentType="application/json",
        )

        if os.path.exists(image_path):
            image_key = f"{prefix}/{base_name}_{timestamp}/{image_filename}"
            s3_client.upload_file(image_path, bucket_name, image_key)

        return {
            "success": True,
            "bucket": bucket_name,
            "json_key": json_key,
            "image_key": image_key if os.path.exists(image_path) else None,
            "timestamp": timestamp,
            "provider": "Amazon S3",
        }

    except ClientError as e:
        return {"success": False, "error": str(e), "provider": "Amazon S3"}
