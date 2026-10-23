"""
image_asset_archive.py - Archive image-analysis artifacts and derived
captions in Amazon S3 managed object storage.

Provider: Amazon S3
SDK: boto3 (service: s3)
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import os
import sys
import json
import io
import datetime
from typing import Optional, Dict, Any

import boto3
from botocore.exceptions import ClientError


def get_s3_client(region_name: Optional[str] = None):
    """
    Create and return an Amazon S3 client using boto3.

    Uses environment variables:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_DEFAULT_REGION (optional)
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    region = region_name or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables "
            "must be set for Amazon S3 access."
        )

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region,
    )

    client = session.client("s3")
    return client


def ensure_bucket_exists(bucket_name: str, region: str = "us-east-1") -> None:
    """Create an S3 bucket if it doesn't already exist."""
    client = get_s3_client()

    try:
        client.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "404":
            if region == "us-east-1":
                client.create_bucket(Bucket=bucket_name)
            else:
                client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={"LocationConstraint": region},
                )
        else:
            raise


def archive_analysis_artifacts(
    bucket_name: str,
    image_name: str,
    analysis_results: Dict[str, Any],
    prefix: str = "image-analysis",
) -> Dict[str, str]:
    """
    Archive image-analysis artifacts and derived captions to Amazon S3.

    Args:
        bucket_name: Target S3 bucket name.
        image_name: Base name of the analyzed image (used for key construction).
        analysis_results: Dict containing all analysis results to archive.
        prefix: S3 key prefix for organizing archived objects.

    Returns:
        Dict mapping artifact types to their S3 object keys.
    """
    client = get_s3_client()
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    safe_image_name = os.path.splitext(os.path.basename(image_name))[0]
    base_key = f"{prefix}/{safe_image_name}/{timestamp}"

    uploaded_keys = {}

    # Upload full analysis results as JSON
    analysis_json = json.dumps(analysis_results, indent=2, default=str)
    analysis_key = f"{base_key}/analysis_results.json"
    client.put_object(
        Bucket=bucket_name,
        Key=analysis_key,
        Body=analysis_json.encode("utf-8"),
        ContentType="application/json",
        Metadata={"image-name": safe_image_name, "timestamp": timestamp},
    )
    uploaded_keys["analysis"] = f"s3://{bucket_name}/{analysis_key}"

    # Upload description/caption separately for easy retrieval
    description = analysis_results.get("description", "")
    if description:
        caption_key = f"{base_key}/caption.txt"
        client.put_object(
            Bucket=bucket_name,
            Key=caption_key,
            Body=description.encode("utf-8"),
            ContentType="text/plain",
            Metadata={"image-name": safe_image_name},
        )
        uploaded_keys["caption"] = f"s3://{bucket_name}/{caption_key}"

    # Upload safety assessment separately
    safety = analysis_results.get("safety_assessment", {})
    if safety:
        safety_json = json.dumps(safety, indent=2)
        safety_key = f"{base_key}/safety_assessment.json"
        client.put_object(
            Bucket=bucket_name,
            Key=safety_key,
            Body=safety_json.encode("utf-8"),
            ContentType="application/json",
        )
        uploaded_keys["safety"] = f"s3://{bucket_name}/{safety_key}"

    # Upload label data
    labels = analysis_results.get("labels", [])
    if labels:
        labels_json = json.dumps(labels, indent=2)
        labels_key = f"{base_key}/labels.json"
        client.put_object(
            Bucket=bucket_name,
            Key=labels_key,
            Body=labels_json.encode("utf-8"),
            ContentType="application/json",
        )
        uploaded_keys["labels"] = f"s3://{bucket_name}/{labels_key}"

    # Upload translated captions if available
    translations = analysis_results.get("translations", {})
    if translations:
        for lang_code, translated_text in translations.items():
            translation_key = f"{base_key}/caption_{lang_code}.txt"
            client.put_object(
                Bucket=bucket_name,
                Key=translation_key,
                Body=translated_text.encode("utf-8"),
                ContentType="text/plain",
                Metadata={"language": lang_code, "image-name": safe_image_name},
            )
            uploaded_keys[f"translation_{lang_code}"] = f"s3://{bucket_name}/{translation_key}"

    return uploaded_keys


def archive_image_file(
    bucket_name: str,
    image_path: str,
    prefix: str = "image-analysis",
) -> str:
    """
    Upload the original image file to S3 alongside analysis artifacts.

    Args:
        bucket_name: Target S3 bucket name.
        image_path: Local path to the image file.
        prefix: S3 key prefix.

    Returns:
        S3 URI of the uploaded image.
    """
    client = get_s3_client()
    image_name = os.path.basename(image_path)
    key = f"{prefix}/{image_name}"

    with open(image_path, "rb") as f:
        client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=f,
            ContentType="image/jpeg",
        )

    return f"s3://{bucket_name}/{key}"


def main():
    """CLI entry point for archiving analysis results to S3."""
    if len(sys.argv) < 3:
        print("Usage: python image_asset_archive.py <bucket_name> <results_json_path> [image_path]")
        sys.exit(1)

    bucket_name = sys.argv[1]
    results_path = sys.argv[2]
    image_path = sys.argv[3] if len(sys.argv) > 3 else None

    if not os.path.exists(results_path):
        print(f"Error: Results file not found: {results_path}")
        sys.exit(1)

    with open(results_path, "r") as f:
        analysis_results = json.load(f)

    image_name = analysis_results.get("image_name", "unknown_image")

    # Upload original image if provided
    if image_path and os.path.exists(image_path):
        image_uri = archive_image_file(bucket_name, image_path)
        print(f"Image archived: {image_uri}")

    # Archive analysis artifacts
    uploaded = archive_analysis_artifacts(bucket_name, image_name, analysis_results)

    print(f"\nArchived artifacts to Amazon S3 bucket: {bucket_name}")
    for artifact_type, s3_uri in uploaded.items():
        print(f"  {artifact_type}: {s3_uri}")


if __name__ == "__main__":
    main()
