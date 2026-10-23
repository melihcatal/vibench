import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import boto3
from botocore.client import Config
from botocore.exceptions import BotoCoreError, ClientError


@dataclass(frozen=True)
class StorageConfig:
    region_name: str
    endpoint_url: Optional[str]
    bucket_name: str
    access_key_id: Optional[str]
    secret_access_key: Optional[str]
    session_token: Optional[str]
    signature_version: str
    addressing_style: str


def load_storage_config() -> StorageConfig:
    return StorageConfig(
        region_name=os.getenv('AWS_REGION') or os.getenv('AWS_DEFAULT_REGION') or 'us-east-1',
        endpoint_url=os.getenv('S3_ENDPOINT_URL') or os.getenv('AWS_ENDPOINT_URL') or os.getenv('MINIO_ENDPOINT'),
        bucket_name=os.getenv('STORAGE_BUCKET') or os.getenv('S3_BUCKET') or '',
        access_key_id=os.getenv('AWS_ACCESS_KEY_ID') or os.getenv('S3_ACCESS_KEY_ID'),
        secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY') or os.getenv('S3_SECRET_ACCESS_KEY'),
        session_token=os.getenv('AWS_SESSION_TOKEN') or os.getenv('S3_SESSION_TOKEN'),
        signature_version=os.getenv('S3_SIGNATURE_VERSION') or 's3v4',
        addressing_style=os.getenv('S3_ADDRESSING_STYLE') or 'virtual',
    )


@lru_cache(maxsize=1)
def get_storage_client():
    config = load_storage_config()
    client_config = Config(signature_version=config.signature_version, s3={'addressing_style': config.addressing_style})
    return boto3.client(
        's3',
        region_name=config.region_name,
        endpoint_url=config.endpoint_url,
        aws_access_key_id=config.access_key_id,
        aws_secret_access_key=config.secret_access_key,
        aws_session_token=config.session_token,
        config=client_config,
    )


def get_bucket_name() -> str:
    bucket_name = load_storage_config().bucket_name
    if not bucket_name:
        raise ValueError('STORAGE_BUCKET or S3_BUCKET must be set')
    return bucket_name


def upload_bytes(key: str, data: bytes, content_type: Optional[str] = None) -> str:
    client = get_storage_client()
    bucket_name = get_bucket_name()
    extra_args = {}
    if content_type:
        extra_args['ContentType'] = content_type
    try:
        client.put_object(Bucket=bucket_name, Key=key, Body=data, **extra_args)
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f'failed to upload {key} to {bucket_name}') from exc
    return key


def download_bytes(key: str) -> bytes:
    client = get_storage_client()
    bucket_name = get_bucket_name()
    try:
        response = client.get_object(Bucket=bucket_name, Key=key)
        return response['Body'].read()
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f'failed to download {key} from {bucket_name}') from exc


def object_exists(key: str) -> bool:
    client = get_storage_client()
    bucket_name = get_bucket_name()
    try:
        client.head_object(Bucket=bucket_name, Key=key)
        return True
    except ClientError as exc:
        error_code = str(exc.response.get('Error', {}).get('Code', ''))
        if error_code in {'404', 'NoSuchKey', 'NotFound'}:
            return False
        raise
