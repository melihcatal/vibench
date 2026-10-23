from __future__ import annotations

import os
import io
from typing import Optional, Union
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from storage_models import (
    UploadRequest,
    UploadResponse,
    PresignedUrlRequest,
    PresignedUrlResponse,
    MetadataRequest,
    MetadataResponse,
    ListPrefixRequest,
    ListPrefixResponse,
    normalize_upload_response,
    normalize_metadata_response,
    normalize_list_response,
    normalize_presigned_response,
)

S3_ENDPOINT = os.getenv("S3_ENDPOINT", "https://s3.amazonaws.com")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
DEFAULT_BUCKET = os.getenv("DEFAULT_BUCKET", "")


def get_s3_client(
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
    endpoint_url: Optional[str] = None,
):
    credentials = {
        "aws_access_key_id": aws_access_key_id or AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": aws_secret_access_key or AWS_SECRET_ACCESS_KEY,
        "region_name": region or AWS_DEFAULT_REGION,
    }
    if endpoint_url:
        credentials["endpoint_url"] = endpoint_url
    elif S3_ENDPOINT:
        credentials["endpoint_url"] = S3_ENDPOINT

    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
        signature_version="s3v4",
    )
    return boto3.client("s3", config=config, **credentials)


def get_textract_client(
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
):
    return boto3.client(
        "textract",
        aws_access_key_id=aws_access_key_id or AWS_ACCESS_KEY_ID,
        aws_secret_access_key=aws_secret_access_key or AWS_SECRET_ACCESS_KEY,
        region_name=region or AWS_DEFAULT_REGION,
    )


def get_translate_client(
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
):
    return boto3.client(
        "translate",
        aws_access_key_id=aws_access_key_id or AWS_ACCESS_KEY_ID,
        aws_secret_access_key=aws_secret_access_key or AWS_SECRET_ACCESS_KEY,
        region_name=region or AWS_DEFAULT_REGION,
    )


def get_bedrock_runtime_client(
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
):
    return boto3.client(
        "bedrock-runtime",
        aws_access_key_id=aws_access_key_id or AWS_ACCESS_KEY_ID,
        aws_secret_access_key=aws_secret_access_key or AWS_SECRET_ACCESS_KEY,
        region_name=region or AWS_DEFAULT_REGION,
    )


def upload_object(
    request: UploadRequest,
    data: Union[bytes, io.BytesIO, str],
    client=None,
) -> UploadResponse:
    if client is None:
        client = get_s3_client()

    extra_args = {}
    if request.content_type:
        extra_args["ContentType"] = request.content_type
    if request.metadata:
        extra_args["Metadata"] = request.metadata
    if request.storage_class:
        extra_args["StorageClass"] = request.storage_class
    if request.server_side_encryption:
        extra_args["ServerSideEncryption"] = request.server_side_encryption

    if isinstance(data, str):
        data = data.encode("utf-8")
    if isinstance(data, bytes):
        data = io.BytesIO(data)

    response = client.put_object(
        Bucket=request.bucket,
        Key=request.key,
        Body=data,
        **extra_args,
    )

    return normalize_upload_response(response, request)


def create_presigned_url(
    request: PresignedUrlRequest,
    client=None,
) -> PresignedUrlResponse:
    if client is None:
        client = get_s3_client()

    url = client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": request.bucket,
            "Key": request.key,
        },
        HttpMethod=request.http_method,
        ExpiresIn=request.expiration_seconds,
    )

    return normalize_presigned_response(url, request)


def get_object_metadata(
    request: MetadataRequest,
    client=None,
) -> MetadataResponse:
    if client is None:
        client = get_s3_client()

    params = {"Bucket": request.bucket, "Key": request.key}
    if request.version_id:
        params["VersionId"] = request.version_id

    response = client.head_object(**params)
    return normalize_metadata_response(response, request)


def list_objects_by_prefix(
    request: ListPrefixRequest,
    client=None,
) -> ListPrefixResponse:
    if client is None:
        client = get_s3_client()

    params = {
        "Bucket": request.bucket,
        "Prefix": request.prefix,
        "MaxKeys": request.max_keys,
    }
    if request.delimiter:
        params["Delimiter"] = request.delimiter
    if request.start_after:
        params["StartAfter"] = request.start_after

    response = client.list_objects_v2(**params)
    return normalize_list_response(response, request)


def get_object_content(
    bucket: str,
    key: str,
    version_id: Optional[str] = None,
    client=None,
) -> bytes:
    if client is None:
        client = get_s3_client()

    params = {"Bucket": bucket, "Key": key}
    if version_id:
        params["VersionId"] = version_id

    response = client.get_object(**params)
    return response["Body"].read()
