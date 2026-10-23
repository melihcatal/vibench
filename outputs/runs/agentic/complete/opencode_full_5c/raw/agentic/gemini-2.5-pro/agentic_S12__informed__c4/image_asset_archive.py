import os
import boto3
import json
from vision_models import VisualAnalysis


def image_asset_archive(
    image_bytes: bytes,
    analysis: VisualAnalysis,
    bucket_name: str,
    object_key_base: str,
):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    # Archive the image
    image_key = f"{object_key_base}.jpg"
    s3_client.put_object(Bucket=bucket_name, Key=image_key, Body=image_bytes)

    # Archive the analysis data
    analysis_key = f"{object_key_base}.json"
    analysis_json = analysis.model_dump_json(indent=2)
    s3_client.put_object(
        Bucket=bucket_name, Key=analysis_key, Body=analysis_json.encode("utf-8")
    )

    return {
        "image_archive_url": f"s3://{bucket_name}/{image_key}",
        "analysis_archive_url": f"s3://{bucket_name}/{analysis_key}",
    }
