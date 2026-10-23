import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

import boto3


@dataclass
class PresignedDownloadResult:
    bucket: str
    key: str
    url: str
    expires_in: int
    expires_at: datetime


def _client():
    return boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
    )


def create_presigned_download_url(
    bucket: str,
    key: str,
    expires_in: int = 3600,
    version_id: Optional[str] = None,
    response_content_disposition: Optional[str] = None,
    response_content_type: Optional[str] = None,
) -> PresignedDownloadResult:
    params = {"Bucket": bucket, "Key": key}
    if version_id:
        params["VersionId"] = version_id
    if response_content_disposition:
        params["ResponseContentDisposition"] = response_content_disposition
    if response_content_type:
        params["ResponseContentType"] = response_content_type
    url = _client().generate_presigned_url(
        ClientMethod="get_object",
        Params=params,
        ExpiresIn=expires_in,
    )
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    return PresignedDownloadResult(bucket=bucket, key=key, url=url, expires_in=expires_in, expires_at=expires_at)
