import boto3
import json
from vision_models import VisionAnalysis, ArchiveResult
import os


def archive_analysis(
    bucket_name: str, asset_id: str, analysis: VisionAnalysis, image_content: bytes
) -> ArchiveResult:
    """Archives image and analysis artifacts to Amazon S3."""
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        region_name=os.environ["AWS_REGION"],
    )

    # Archive original image
    image_key = f"{asset_id}.jpg"
    s3_client.put_object(Bucket=bucket_name, Key=image_key, Body=image_content)

    # Archive analysis data
    analysis_key = f"{asset_id}_analysis.json"
    analysis_json = analysis.model_dump_json()
    response = s3_client.put_object(
        Bucket=bucket_name, Key=analysis_key, Body=analysis_json
    )

    return ArchiveResult(
        bucket=bucket_name,
        key=analysis_key,
        VersionId=response.get("VersionId"),
        ETag=response.get("ETag"),
    )
