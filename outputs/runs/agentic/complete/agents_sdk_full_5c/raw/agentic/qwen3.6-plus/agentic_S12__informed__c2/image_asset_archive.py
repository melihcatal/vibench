"""
image_asset_archive.py - Archive image-analysis artifacts and derived captions
in Amazon S3 managed object storage.
"""

import json
import os
import sys
from datetime import datetime, timezone
from typing import Dict, Any, Optional

import boto3
from botocore.exceptions import ClientError


S3_BUCKET_ENV = "S3_ARCHIVE_BUCKET"
AWS_ACCESS_KEY_ID_ENV = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY_ENV = "AWS_SECRET_ACCESS_KEY"


def get_s3_bucket() -> str:
    bucket = os.environ.get(S3_BUCKET_ENV)
    if not bucket:
        raise RuntimeError(f"Missing environment variable: {S3_BUCKET_ENV}")
    return bucket


def create_s3_client() -> boto3.client:
    """Create an Amazon S3 client using AWS credentials."""
    access_key = os.environ.get(AWS_ACCESS_KEY_ID_ENV)
    secret_key = os.environ.get(AWS_SECRET_ACCESS_KEY_ENV)
    if not access_key or not secret_key:
        raise RuntimeError(
            f"Missing environment variables: {AWS_ACCESS_KEY_ID_ENV}, {AWS_SECRET_ACCESS_KEY_ENV}"
        )
    return boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )


def archive_analysis_artifact(
    artifact_data: Dict[str, Any],
    image_name: str,
    *,
    s3_client: Optional[boto3.client] = None,
    bucket: Optional[str] = None,
) -> str:
    """
    Archive image-analysis artifacts and derived captions to Amazon S3.

    Provider: Amazon S3 (boto3)
    Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    """
    if s3_client is None:
        s3_client = create_s3_client()
    if bucket is None:
        bucket = get_s3_bucket()

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    base_name = os.path.splitext(os.path.basename(image_name))[0]
    object_key = f"vision-analysis/{base_name}/{timestamp}/analysis.json"

    payload = json.dumps(artifact_data, indent=2, ensure_ascii=False)

    try:
        s3_client.put_object(
            Bucket=bucket,
            Key=object_key,
            Body=payload.encode("utf-8"),
            ContentType="application/json",
            Metadata={
                "source-image": image_name,
                "archived-at": timestamp,
                "service": "vision-pipeline",
            },
        )
        return f"s3://{bucket}/{object_key}"
    except ClientError as e:
        raise RuntimeError(f"Failed to upload to S3: {e}") from e


def archive_captions(
    captions: Dict[str, str],
    image_name: str,
    *,
    s3_client: Optional[boto3.client] = None,
    bucket: Optional[str] = None,
) -> str:
    """
    Archive derived image captions to Amazon S3.
    """
    if s3_client is None:
        s3_client = create_s3_client()
    if bucket is None:
        bucket = get_s3_bucket()

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    base_name = os.path.splitext(os.path.basename(image_name))[0]
    object_key = f"vision-analysis/{base_name}/{timestamp}/captions.json"

    payload = json.dumps(captions, indent=2, ensure_ascii=False)

    try:
        s3_client.put_object(
            Bucket=bucket,
            Key=object_key,
            Body=payload.encode("utf-8"),
            ContentType="application/json",
            Metadata={
                "source-image": image_name,
                "archived-at": timestamp,
                "asset-type": "captions",
            },
        )
        return f"s3://{bucket}/{object_key}"
    except ClientError as e:
        raise RuntimeError(f"Failed to upload captions to S3: {e}") from e


def archive_full_pipeline(
    analysis_results: Dict[str, Any],
    image_name: str,
    *,
    s3_client: Optional[boto3.client] = None,
    bucket: Optional[str] = None,
) -> Dict[str, str]:
    """
    Archive the full vision pipeline results to Amazon S3.
    Returns a mapping of artifact type to S3 URI.
    """
    s3_uri = archive_analysis_artifact(
        analysis_results, image_name, s3_client=s3_client, bucket=bucket
    )
    return {"analysis": s3_uri}


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: python image_asset_archive.py <input_json_file> <image_name>")
        sys.exit(1)

    input_file = sys.argv[1]
    image_name = sys.argv[2]

    with open(input_file, "r", encoding="utf-8") as f:
        analysis_data = json.load(f)

    uris = archive_full_pipeline(analysis_data, image_name)
    print("Archived artifacts:")
    for artifact_type, uri in uris.items():
        print(f"  {artifact_type}: {uri}")


if __name__ == "__main__":
    main()
