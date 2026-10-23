import os
import io
from typing import Optional, Union

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError, BotoCoreError

from storage_models import StorageConfig


def get_s3_client(config: Optional[StorageConfig] = None):
    if config is None:
        config = StorageConfig.from_env()

    botocore_config = Config(
        retries={"max_attempts": config.max_retries, "mode": "adaptive"},
        connect_timeout=config.connection_timeout,
        read_timeout=config.read_timeout,
        signature_version="s3v4",
    )

    session = boto3.Session(
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
        region_name=config.aws_region,
    )

    client_kwargs = {"config": botocore_config}
    if config.endpoint_url:
        client_kwargs["endpoint_url"] = config.endpoint_url

    return session.client("s3", **client_kwargs)


def get_s3_resource(config: Optional[StorageConfig] = None):
    if config is None:
        config = StorageConfig.from_env()

    botocore_config = Config(
        retries={"max_attempts": config.max_retries, "mode": "adaptive"},
        connect_timeout=config.connection_timeout,
        read_timeout=config.read_timeout,
        signature_version="s3v4",
    )

    session = boto3.Session(
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
        region_name=config.aws_region,
    )

    resource_kwargs = {"config": botocore_config}
    if config.endpoint_url:
        resource_kwargs["endpoint_url"] = config.endpoint_url

    return session.resource("s3", **resource_kwargs)


def get_textract_client(config: Optional[StorageConfig] = None):
    if config is None:
        config = StorageConfig.from_env()

    botocore_config = Config(
        retries={"max_attempts": config.max_retries, "mode": "adaptive"},
        connect_timeout=config.connection_timeout,
        read_timeout=config.read_timeout,
    )

    session = boto3.Session(
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
        region_name=config.aws_region,
    )

    return session.client("textract", config=botocore_config)


def get_translate_client(config: Optional[StorageConfig] = None):
    if config is None:
        config = StorageConfig.from_env()

    botocore_config = Config(
        retries={"max_attempts": config.max_retries, "mode": "adaptive"},
        connect_timeout=config.connection_timeout,
        read_timeout=config.read_timeout,
    )

    session = boto3.Session(
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
        region_name=config.aws_region,
    )

    return session.client("translate", config=botocore_config)


def get_bedrock_runtime_client(config: Optional[StorageConfig] = None):
    if config is None:
        config = StorageConfig.from_env()

    botocore_config = Config(
        retries={"max_attempts": config.max_retries, "mode": "adaptive"},
        connect_timeout=config.connection_timeout,
        read_timeout=config.read_timeout,
    )

    session = boto3.Session(
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
        region_name=config.aws_region,
    )

    return session.client("bedrock-runtime", config=botocore_config)


def normalize_metadata_response(raw_response: dict, bucket: str, key: str) -> dict:
    headers = raw_response.get("ResponseMetadata", {}).get("HTTPHeaders", {})
    return {
        "content_type": raw_response.get(
            "ContentType", headers.get("content-type", "")
        ),
        "content_length": int(
            raw_response.get("ContentLength", headers.get("content-length", 0))
        ),
        "last_modified": raw_response.get("LastModified"),
        "etag": raw_response.get("ETag", "").strip('"'),
        "version_id": raw_response.get("VersionId"),
        "storage_class": raw_response.get("StorageClass", ""),
        "metadata": {k: v for k, v in raw_response.get("Metadata", {}).items()},
    }


def normalize_list_objects_response(raw_response: dict) -> dict:
    objects = []
    for item in raw_response.get("Contents", []):
        objects.append(
            {
                "key": item["Key"],
                "size": item.get("Size", 0),
                "last_modified": item.get("LastModified"),
                "etag": item.get("ETag", "").strip('"'),
                "storage_class": item.get("StorageClass", ""),
            }
        )

    common_prefixes = [
        p.get("Prefix", "") for p in raw_response.get("CommonPrefixes", [])
    ]

    return {
        "objects": objects,
        "common_prefixes": common_prefixes,
        "is_truncated": raw_response.get("IsTruncated", False),
        "next_continuation_token": raw_response.get("NextContinuationToken"),
        "key_count": raw_response.get("KeyCount", len(objects)),
    }


def handle_aws_error(error: Exception, operation: str) -> str:
    if isinstance(error, ClientError):
        error_code = error.response["Error"]["Code"]
        error_message = error.response["Error"]["Message"]
        return f"AWS {operation} error [{error_code}]: {error_message}"
    elif isinstance(error, BotoCoreError):
        return f"AWS {operation} client error: {str(error)}"
    return f"{operation} error: {str(error)}"


def read_object_content(
    s3_client, bucket: str, key: str, version_id: Optional[str] = None
) -> bytes:
    get_kwargs = {"Bucket": bucket, "Key": key}
    if version_id:
        get_kwargs["VersionId"] = version_id

    response = s3_client.get_object(**get_kwargs)
    return response["Body"].read()


def stream_object_content(s3_client, bucket: str, key: str, chunk_size: int = 8192):
    response = s3_client.get_object(Bucket=bucket, Key=key)
    body = response["Body"]
    for chunk in body.iter_chunks(chunk_size=chunk_size):
        yield chunk
