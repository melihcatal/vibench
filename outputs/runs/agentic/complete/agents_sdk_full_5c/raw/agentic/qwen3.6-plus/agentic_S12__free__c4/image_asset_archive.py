"""
Archive image-analysis artifacts and derived captions in managed object storage using AWS S3.
Provider: AWS S3 (boto3)
Endpoint: s3.amazonaws.com
Service: Amazon Simple Storage Service
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from typing import Optional

import boto3
from botocore.exceptions import ClientError


def get_s3_client(
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
) -> boto3.client:
    """
    Initialize and return an AWS S3 client.

    Args:
        aws_access_key_id: AWS access key ID. Falls back to environment variables.
        aws_secret_access_key: AWS secret access key. Falls back to environment variables.
        region: AWS region (e.g., 'us-east-1'). Falls back to AWS_DEFAULT_REGION.

    Returns:
        Configured boto3 S3 client.
    """
    session_kwargs = {}
    if aws_access_key_id:
        session_kwargs["aws_access_key_id"] = aws_access_key_id
    if aws_secret_access_key:
        session_kwargs["aws_secret_access_key"] = aws_secret_access_key
    if region:
        session_kwargs["region_name"] = region

    session = boto3.Session(**session_kwargs)
    return session.client("s3")


def compute_asset_hash(file_path: Optional[str] = None, content: Optional[bytes] = None) -> str:
    """
    Compute SHA-256 hash for an asset file or content bytes.

    Args:
        file_path: Path to the file to hash.
        content: Raw bytes to hash.

    Returns:
        Hex digest string.
    """
    if file_path:
        with open(file_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    elif content:
        return hashlib.sha256(content).hexdigest()
    raise ValueError("Either file_path or content must be provided")


def archive_image_analysis(
    bucket_name: str,
    image_source: str,
    analysis_results: dict,
    image_path: Optional[str] = None,
    prefix: str = "image-analysis",
    s3_client: Optional[boto3.client] = None,
    metadata: Optional[dict] = None,
) -> dict:
    """
    Archive image-analysis artifacts and derived captions to AWS S3.

    Uploads the analysis results as JSON metadata and optionally the source image,
    organized under a structured prefix in S3.

    Args:
        bucket_name: Target S3 bucket name.
        image_source: Original image path or URI for identification.
        analysis_results: Dictionary containing labels, descriptions, text, safety data.
        image_path: Optional local path to the source image for upload.
        prefix: S3 key prefix (default: 'image-analysis').
        s3_client: Optional pre-configured S3 client.
        metadata: Optional additional metadata to attach.

    Returns:
        Dictionary with S3 key, ETag, and upload status.
    """
    if not s3_client:
        s3_client = get_s3_client()

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    image_basename = os.path.basename(image_source) if image_source else "unknown"
    image_hash = compute_asset_hash(file_path=image_path) if image_path else hashlib.sha256(image_source.encode()).hexdigest()[:16]

    archive_key = f"{prefix}/{timestamp}/{image_hash}/{image_basename}"

    analysis_payload = {
        "image_source": image_source,
        "image_hash": image_hash,
        "archived_at": timestamp,
        "provider": "google_cloud_vision",
        "analysis": analysis_results,
    }

    if metadata:
        analysis_payload["metadata"] = metadata

    try:
        analysis_json = json.dumps(analysis_payload, indent=2, default=str)

        analysis_response = s3_client.put_object(
            Bucket=bucket_name,
            Key=f"{archive_key}/analysis.json",
            Body=analysis_json.encode("utf-8"),
            ContentType="application/json",
            Metadata={
                "image-hash": image_hash,
                "archived-at": timestamp,
                "source": image_source[:200],
            },
        )

        image_upload_result = None
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                image_response = s3_client.put_object(
                    Bucket=bucket_name,
                    Key=f"{archive_key}/source.{os.path.splitext(image_path)[1].lstrip('.') or 'bin'}",
                    Body=img_file.read(),
                    ContentType="application/octet-stream",
                )
                image_upload_result = {
                    "key": f"{archive_key}/source",
                    "etag": image_response.get("ETag", "").strip('"'),
                }

        return {
            "provider": "aws_s3",
            "bucket": bucket_name,
            "archive_key": archive_key,
            "analysis_key": f"{archive_key}/analysis.json",
            "analysis_etag": analysis_response.get("ETag", "").strip('"'),
            "image_upload": image_upload_result,
            "status": "success",
            "timestamp": timestamp,
        }

    except ClientError as exc:
        return {
            "provider": "aws_s3",
            "bucket": batch_name,
            "status": "error",
            "error": str(exc),
        }


def archive_batch_analyses(
    bucket_name: str,
    analyses: list[dict],
    prefix: str = "image-analysis",
) -> list[dict]:
    """
    Archive multiple image analyses to S3 in batch.

    Args:
        bucket_name: Target S3 bucket name.
        analyses: List of analysis result dictionaries, each with 'image_source' and 'results'.
        prefix: S3 key prefix.

    Returns:
        List of archive result dictionaries.
    """
    s3_client = get_s3_client()
    results = []

    for item in analyses:
        result = archive_image_analysis(
            bucket_name=bucket_name,
            image_source=item.get("image_source", "unknown"),
            analysis_results=item.get("results", {}),
            image_path=item.get("image_path"),
            prefix=prefix,
            s3_client=s3_client,
            metadata=item.get("metadata"),
        )
        results.append(result)

    return results


def list_archived_analyses(
    bucket_name: str,
    prefix: str = "image-analysis",
    max_keys: int = 100,
) -> list[dict]:
    """
    List archived image analyses in S3.

    Args:
        bucket_name: S3 bucket name.
        prefix: S3 key prefix to filter by.
        max_keys: Maximum number of results to return.

    Returns:
        List of archived analysis metadata dictionaries.
    """
    s3_client = get_s3_client()

    response = s3_client.list_objects_v2(
        Bucket=bucket_name,
        Prefix=prefix,
        MaxKeys=max_keys,
    )

    objects = response.get("Contents", [])
    return [
        {
            "key": obj["Key"],
            "size": obj["Size"],
            "last_modified": obj["LastModified"].isoformat(),
            "etag": obj["ETag"].strip('"'),
        }
        for obj in objects
        if obj["Key"].endswith("analysis.json")
    ]


def get_archived_analysis(
    bucket_name: str,
    archive_key: str,
) -> Optional[dict]:
    """
    Retrieve an archived analysis from S3.

    Args:
        bucket_name: S3 bucket name.
        archive_key: S3 key for the analysis.json file.

    Returns:
        Parsed analysis dictionary or None if not found.
    """
    s3_client = get_s3_client()

    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=archive_key)
        content = response["Body"].read().decode("utf-8")
        return json.loads(content)
    except ClientError:
        return None


if __name__ == "__main__":
    import sys

    bucket = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("AWS_S3_BUCKET")
    if bucket:
        sample_results = {
            "labels": [{"label": "test", "confidence": 0.95}],
            "description": "Test image",
            "safety": {"is_safe": True},
        }
        result = archive_image_analysis(
            bucket_name=bucket,
            image_source="test.jpg",
            analysis_results=sample_results,
        )
        print(json.dumps(result, indent=2))
