import os
import json
import io
from typing import Optional, Dict, Any, List
import boto3
from botocore.exceptions import ClientError


AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
S3_BUCKET = os.environ.get("S3_BUCKET", "image-analysis-archive")
S3_REGION = os.environ.get("AWS_REGION", "us-east-1")


def get_s3_client():
    return boto3.client(
        "s3",
        region_name=S3_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )


def archive_image_asset(
    s3_key: str,
    image_bytes: bytes,
    metadata: Optional[Dict[str, Any]] = None,
    content_type: str = "image/jpeg",
) -> Dict[str, Any]:
    client = get_s3_client()
    upload_kwargs = {
        "Bucket": S3_BUCKET,
        "Key": s3_key,
        "Body": image_bytes,
        "ContentType": content_type,
    }
    if metadata:
        upload_kwargs["Metadata"] = {k: str(v) for k, v in metadata.items()}
    client.put_object(**upload_kwargs)
    return {"bucket": S3_BUCKET, "key": s3_key, "status": "uploaded"}


def archive_analysis_artifact(
    artifact_key: str,
    artifact_data: Dict[str, Any],
) -> Dict[str, Any]:
    client = get_s3_client()
    json_bytes = json.dumps(artifact_data, indent=2).encode("utf-8")
    client.put_object(
        Bucket=S3_BUCKET,
        Key=artifact_key,
        Body=json_bytes,
        ContentType="application/json",
    )
    return {"bucket": S3_BUCKET, "key": artifact_key, "status": "uploaded"}


def archive_captions(
    captions: List[Dict[str, str]],
    prefix: str = "captions",
) -> Dict[str, Any]:
    client = get_s3_client()
    combined = {"captions": captions}
    json_bytes = json.dumps(combined, indent=2).encode("utf-8")
    artifact_key = f"{prefix}/captions_bundle.json"
    client.put_object(
        Bucket=S3_BUCKET,
        Key=artifact_key,
        Body=json_bytes,
        ContentType="application/json",
    )
    return {"bucket": S3_BUCKET, "key": artifact_key, "status": "uploaded"}


def archive_full_pipeline(
    image_key: str,
    image_bytes: bytes,
    labels_data: Optional[Dict[str, Any]] = None,
    description_data: Optional[Dict[str, Any]] = None,
    text_data: Optional[Dict[str, Any]] = None,
    safety_data: Optional[Dict[str, Any]] = None,
    summary: Optional[str] = None,
    translations: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, Any]:
    results = {}
    results["image"] = archive_image_asset(image_key, image_bytes)
    artifacts = {}
    if labels_data:
        artifacts["labels"] = labels_data
    if description_data:
        artifacts["description"] = description_data
    if text_data:
        artifacts["text"] = text_data
    if safety_data:
        artifacts["safety"] = safety_data
    if summary:
        artifacts["summary"] = summary
    if translations:
        artifacts["translations"] = translations
    if artifacts:
        results["analysis"] = archive_analysis_artifact(
            image_key.replace(".jpg", "_analysis.json").replace(
                ".png", "_analysis.json"
            ),
            artifacts,
        )
    return results


if __name__ == "__main__":
    print(f"Archive target: s3://{S3_BUCKET}/")
