import json
import os

import boto3

from vision_models import (
    ArchiveManifest,
    ImageDescriptionResult,
    LabelDetectionResult,
    TextDetectionResult,
    VisualAnalysisSummary,
)


def archive_image_assets(
    image_path: str,
    labels_result: LabelDetectionResult,
    description_result: ImageDescriptionResult,
    text_result: TextDetectionResult,
    summary: VisualAnalysisSummary,
) -> ArchiveManifest:
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID", "")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    bucket = os.environ.get("S3_BUCKET_NAME", "image-analysis-artifacts")
    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise RuntimeError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required"
        )

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region,
    )

    base_key = image_path.replace("/", "_").replace(".", "_")
    uploaded = []

    labels_payload = {
        "image_path": labels_result.image_path,
        "labels": [
            {"label": l.label, "confidence": l.confidence, "category": l.category}
            for l in labels_result.labels
        ],
    }
    s3_client.put_object(
        Bucket=bucket,
        Key=f"{base_key}/labels.json",
        Body=json.dumps(labels_payload, indent=2),
        ContentType="application/json",
    )
    uploaded.append(f"{base_key}/labels.json")

    description_payload = {
        "image_path": description_result.image_path,
        "description": description_result.description,
        "confidence": description_result.confidence,
    }
    s3_client.put_object(
        Bucket=bucket,
        Key=f"{base_key}/description.json",
        Body=json.dumps(description_payload, indent=2),
        ContentType="application/json",
    )
    uploaded.append(f"{base_key}/description.json")

    text_payload = {
        "image_path": text_result.image_path,
        "full_text": text_result.full_text,
        "annotation_count": len(text_result.annotations),
    }
    s3_client.put_object(
        Bucket=bucket,
        Key=f"{base_key}/text.json",
        Body=json.dumps(text_payload, indent=2),
        ContentType="application/json",
    )
    uploaded.append(f"{base_key}/text.json")

    summary_payload = {
        "image_path": summary.image_path,
        "description": summary.description,
        "labels": summary.labels,
        "detected_text": summary.detected_text,
        "safety_is_safe": summary.safety_is_safe,
        "summary": summary.summary,
    }
    s3_client.put_object(
        Bucket=bucket,
        Key=f"{base_key}/summary.json",
        Body=json.dumps(summary_payload, indent=2),
        ContentType="application/json",
    )
    uploaded.append(f"{base_key}/summary.json")

    return ArchiveManifest(
        image_path=image_path,
        archive_key=f"{base_key}/",
        uploaded_objects=uploaded,
    )
