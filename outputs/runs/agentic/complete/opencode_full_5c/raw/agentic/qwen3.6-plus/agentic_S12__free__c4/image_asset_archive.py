import os
import json
import datetime
import boto3
from botocore.exceptions import ClientError
from vision_models import VisionAnalysisResult, ImageDescription


def get_s3_client():
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required"
        )
    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )
    client = session.client("s3", endpoint_url="https://s3.amazonaws.com")
    return client


def archive_analysis_result(
    result: VisionAnalysisResult,
    bucket: str,
    key_prefix: str = "vision-analysis",
    s3_client=None,
) -> dict:
    if s3_client is None:
        s3_client = get_s3_client()
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    labels_data = [
        {"name": l.name, "confidence": l.confidence, "category": l.category}
        for l in result.labels
    ]
    texts_data = [
        {"text": t.text, "confidence": t.confidence} for t in result.detected_texts
    ]
    safety_data = {
        "is_safe": result.safety.is_safe if result.safety else None,
        "overall_score": result.safety.overall_score if result.safety else None,
        "flagged_categories": result.safety.flagged_categories if result.safety else [],
    }
    desc_data = {
        "description": result.description.description if result.description else "",
        "summary": result.description.summary if result.description else "",
    }
    payload = {
        "timestamp": timestamp,
        "labels": labels_data,
        "description": desc_data,
        "detected_texts": texts_data,
        "safety": safety_data,
    }
    analysis_key = f"{key_prefix}/analysis-{timestamp}.json"
    s3_client.put_object(
        Bucket=bucket,
        Key=analysis_key,
        Body=json.dumps(payload, indent=2),
        ContentType="application/json",
    )
    return {"bucket": bucket, "key": analysis_key, "timestamp": timestamp}


def archive_image_file(
    image_path: str,
    bucket: str,
    key_prefix: str = "vision-analysis/images",
    s3_client=None,
) -> dict:
    if s3_client is None:
        s3_client = get_s3_client()
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    filename = os.path.basename(image_path)
    object_key = f"{key_prefix}/{timestamp}-{filename}"
    with open(image_path, "rb") as f:
        s3_client.put_object(
            Bucket=bucket,
            Key=object_key,
            Body=f.read(),
            ContentType="image/jpeg",
        )
    return {"bucket": bucket, "key": object_key}


def archive_caption(
    caption: ImageDescription,
    bucket: str,
    key_prefix: str = "vision-analysis/captions",
    s3_client=None,
) -> dict:
    if s3_client is None:
        s3_client = get_s3_client()
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    caption_data = {
        "timestamp": timestamp,
        "description": caption.description,
        "summary": caption.summary,
        "tags": caption.tags,
    }
    caption_key = f"{key_prefix}/caption-{timestamp}.json"
    s3_client.put_object(
        Bucket=bucket,
        Key=caption_key,
        Body=json.dumps(caption_data, indent=2),
        ContentType="application/json",
    )
    return {"bucket": bucket, "key": caption_key, "timestamp": timestamp}


def archive_all_artifacts(
    result: VisionAnalysisResult,
    image_path: str = None,
    bucket: str = None,
    s3_client=None,
) -> dict:
    if bucket is None:
        bucket = os.environ.get("VISION_ARCHIVE_BUCKET", "vision-analysis-archive")
    artifacts = {}
    artifacts["analysis"] = archive_analysis_result(result, bucket, s3_client=s3_client)
    if result.description:
        artifacts["caption"] = archive_caption(
            result.description, bucket, s3_client=s3_client
        )
    if image_path and os.path.exists(image_path):
        artifacts["image"] = archive_image_file(image_path, bucket, s3_client=s3_client)
    return artifacts


if __name__ == "__main__":
    from vision_models import ImageLabel, SafetyScore

    sample = VisionAnalysisResult(
        labels=[ImageLabel("mountain", 0.96, "nature")],
        description=ImageDescription(description="A snow-capped mountain at sunrise."),
        safety=SafetyScore(is_safe=True, overall_score=0.99),
    )
    print("Archive ready. Set AWS credentials and VISION_ARCHIVE_BUCKET to upload.")
