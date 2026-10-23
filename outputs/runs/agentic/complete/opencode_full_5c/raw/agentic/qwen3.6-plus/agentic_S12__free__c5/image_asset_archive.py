import os
import json
import datetime
import hashlib
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from vision_models import ArchiveRequest, ArchiveResponse, VisionAnalysisResponse


AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "image-analysis-artifacts")


def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )


def generate_archive_key(prefix: str, image_path: str) -> str:
    filename = os.path.basename(image_path)
    name_without_ext = os.path.splitext(filename)[0]
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    file_hash = hashlib.md5(image_path.encode("utf-8")).hexdigest()[:8]
    return f"{prefix}/{name_without_ext}/{timestamp}_{file_hash}"


def archive_analysis_results(request: ArchiveRequest) -> ArchiveResponse:
    s3 = get_s3_client()
    archive_key = generate_archive_key(request.archive_key_prefix, request.image_path)
    archived_files = []

    analysis_json = {
        "image_path": request.image_path,
        "labels": [
            {"name": l.name, "confidence": l.confidence, "category": l.category}
            for l in request.analysis_results.labels
        ],
        "description": request.analysis_results.description,
        "detected_text": [
            {"text": t.text, "confidence": t.confidence}
            for t in request.analysis_results.detected_text
        ],
        "safety": {
            "is_safe": request.analysis_results.safety.is_safe
            if request.analysis_results.safety
            else None,
            "categories": request.analysis_results.safety.categories
            if request.analysis_results.safety
            else {},
            "flagged_categories": request.analysis_results.safety.flagged_categories
            if request.analysis_results.safety
            else [],
        }
        if request.analysis_results.safety
        else None,
        "raw_output": request.analysis_results.raw_output,
        "archived_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }

    analysis_key = f"{archive_key}/analysis.json"
    s3.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=analysis_key,
        Body=json.dumps(analysis_json, indent=2),
        ContentType="application/json",
    )
    archived_files.append(analysis_key)

    if request.summary:
        summary_key = f"{archive_key}/summary.txt"
        s3.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=summary_key,
            Body=request.summary,
            ContentType="text/plain",
        )
        archived_files.append(summary_key)

    if request.alt_text:
        alt_text_key = f"{archive_key}/alt_text.txt"
        s3.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=alt_text_key,
            Body=request.alt_text,
            ContentType="text/plain",
        )
        archived_files.append(alt_text_key)

    try:
        with open(request.image_path, "rb") as f:
            image_data = f.read()
        image_key = f"{archive_key}/source_image"
        ext = os.path.splitext(request.image_path)[1].lower()
        content_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
        }
        s3.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=f"{image_key}{ext}",
            Body=image_data,
            ContentType=content_types.get(ext, "application/octet-stream"),
        )
        archived_files.append(f"{image_key}{ext}")
    except FileNotFoundError:
        pass

    archive_url = (
        f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{archive_key}"
    )

    return ArchiveResponse(
        archive_url=archive_url,
        archived_files=archived_files,
        status="completed",
    )


def archive_batch(requests: list[ArchiveRequest]) -> list[ArchiveResponse]:
    results = []
    for req in requests:
        result = archive_analysis_results(req)
        results.append(result)
    return results


def list_archived_artifacts(prefix: str) -> list[str]:
    s3 = get_s3_client()
    keys = []
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=S3_BUCKET_NAME, Prefix=prefix):
        for obj in page.get("Contents", []):
            keys.append(obj["Key"])
    return keys
