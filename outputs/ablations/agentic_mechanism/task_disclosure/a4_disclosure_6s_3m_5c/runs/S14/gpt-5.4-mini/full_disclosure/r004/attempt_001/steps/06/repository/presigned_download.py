import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


@dataclass
class PresignedDownloadResult:
    bucket: str
    key: str
    url: str
    expires_in: int
    expires_at: datetime


def _s3_client(region_name: Optional[str] = None):
    return boto3.client("s3", region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))


def create_presigned_download_url(
    bucket: str,
    key: str,
    expires_in: int = 3600,
    region_name: Optional[str] = None,
    download_filename: Optional[str] = None,
    response_content_type: Optional[str] = None,
) -> PresignedDownloadResult:
    if expires_in <= 0:
        raise ValueError("expires_in must be greater than 0")
    client = _s3_client(region_name)
    params = {"Bucket": bucket, "Key": key}
    if download_filename:
        params["ResponseContentDisposition"] = f'attachment; filename="{download_filename}"'
    if response_content_type:
        params["ResponseContentType"] = response_content_type
    try:
        url = client.generate_presigned_url(
            ClientMethod="get_object",
            Params=params,
            ExpiresIn=expires_in,
        )
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"failed to create presigned download url for s3://{bucket}/{key}: {exc}") from exc
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    return PresignedDownloadResult(bucket=bucket, key=key, url=url, expires_in=expires_in, expires_at=expires_at)
