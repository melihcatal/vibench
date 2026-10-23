import os
from dataclasses import asdict
from typing import Any, Dict, Optional

import boto3
from botocore.client import Config

from storage_models import (
    ListPrefixResponse,
    ObjectMetadataResponse,
    PresignedDownloadResponse,
    UploadObjectResponse,
)


def get_storage_config() -> Dict[str, Any]:
    return {
        "aws_region": os.getenv(
            "AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        ),
        "aws_profile": os.getenv("AWS_PROFILE"),
        "s3_endpoint_url": os.getenv("S3_ENDPOINT_URL"),
        "signature_version": os.getenv("S3_SIGNATURE_VERSION", "s3v4"),
    }


def get_s3_client():
    config = get_storage_config()
    session = boto3.session.Session(
        profile_name=config["aws_profile"], region_name=config["aws_region"]
    )
    return session.client(
        "s3",
        endpoint_url=config["s3_endpoint_url"],
        config=Config(signature_version=config["signature_version"]),
    )


def to_dict(response: Any) -> Dict[str, Any]:
    if hasattr(response, "__dict__"):
        return dict(response.__dict__)
    return dict(response)


def build_upload_response(
    bucket: str, key: str, result: Dict[str, Any]
) -> UploadObjectResponse:
    return UploadObjectResponse(
        bucket=bucket,
        key=key,
        etag=result.get("ETag"),
        version_id=result.get("VersionId"),
    )


def build_metadata_response(
    bucket: str, key: str, head: Dict[str, Any]
) -> ObjectMetadataResponse:
    return ObjectMetadataResponse(
        bucket=bucket,
        key=key,
        content_length=head.get("ContentLength"),
        content_type=head.get("ContentType"),
        etag=head.get("ETag"),
        last_modified=str(head.get("LastModified"))
        if head.get("LastModified")
        else None,
        metadata=head.get("Metadata") or {},
    )


def build_list_response(
    bucket: str, prefix: str, keys: list[str]
) -> ListPrefixResponse:
    return ListPrefixResponse(bucket=bucket, prefix=prefix, keys=keys)


def build_presigned_download_response(
    bucket: str, key: str, url: str, expires_in: int
) -> PresignedDownloadResponse:
    return PresignedDownloadResponse(
        bucket=bucket, key=key, url=url, expires_in=expires_in
    )
