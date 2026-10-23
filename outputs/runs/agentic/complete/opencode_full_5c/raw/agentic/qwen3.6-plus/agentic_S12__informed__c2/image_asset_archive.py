import os
import json
import io
import boto3
from botocore.exceptions import ClientError
from vision_models import VisualAnalysisResult, result_to_dict


AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "image-analysis-archive")
S3_REGION = os.environ.get("S3_REGION", "us-east-1")


def archive_image_analysis(
    image_url: str,
    analysis_result: VisualAnalysisResult,
    summary: str = "",
    translations: list[dict] = None,
    safety_text_result: dict = None,
    archive_key: str = None,
) -> dict:
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set")
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=S3_REGION,
    )
    if archive_key is None:
        import hashlib

        image_hash = hashlib.md5(image_url.encode()).hexdigest()[:12]
        archive_key = f"analysis-results/{image_hash}/manifest.json"
    manifest = _build_manifest(
        image_url=image_url,
        analysis_result=analysis_result,
        summary=summary,
        translations=translations or [],
        safety_text_result=safety_text_result,
    )
    manifest_bytes = json.dumps(manifest, indent=2).encode("utf-8")
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=archive_key,
            Body=manifest_bytes,
            ContentType="application/json",
        )
    except ClientError as e:
        raise RuntimeError(f"Failed to upload to S3: {e}")
    return {
        "bucket": S3_BUCKET_NAME,
        "key": archive_key,
        "region": S3_REGION,
        "s3_uri": f"s3://{S3_BUCKET_NAME}/{archive_key}",
    }


def archive_captions(
    captions: list[dict],
    archive_key: str = None,
) -> dict:
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set")
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=S3_REGION,
    )
    if archive_key is None:
        archive_key = "analysis-results/captions/captions.json"
    captions_bytes = json.dumps(captions, indent=2).encode("utf-8")
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=archive_key,
            Body=captions_bytes,
            ContentType="application/json",
        )
    except ClientError as e:
        raise RuntimeError(f"Failed to upload captions to S3: {e}")
    return {
        "bucket": S3_BUCKET_NAME,
        "key": archive_key,
        "region": S3_REGION,
        "s3_uri": f"s3://{S3_BUCKET_NAME}/{archive_key}",
    }


def _build_manifest(
    image_url: str,
    analysis_result: VisualAnalysisResult,
    summary: str,
    translations: list[dict],
    safety_text_result: dict,
) -> dict:
    return {
        "image_url": image_url,
        "analysis": result_to_dict(analysis_result),
        "summary": summary,
        "translations": translations,
        "safety_text_check": safety_text_result,
    }
