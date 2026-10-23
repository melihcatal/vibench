"""
presigned_download.py — Create a time-limited signed download URL for a stored object.

Concrete provider: Amazon S3 via boto3 SDK.
Provider signals:
  - boto3 S3 generate_presigned_url usage
  - S3 client from storage_client
"""

from typing import Optional
from botocore.exceptions import ClientError

from storage_client import S3StorageClient
from storage_models import PresignedUrlResult


def create_presigned_download_url(
    bucket: str,
    key: str,
    expires_in_seconds: int = 3600,
    response_content_disposition: Optional[str] = None,
    response_content_type: Optional[str] = None,
) -> PresignedUrlResult:
    """
    Generate a presigned URL for downloading an S3 object.

    The URL is valid for ``expires_in_seconds`` and grants GET access
    without requiring AWS credentials on the client side.

    Parameters
    ----------
    bucket : str
        S3 bucket containing the object.
    key : str
        S3 object key.
    expires_in_seconds : int
        Lifetime of the presigned URL in seconds (default 3600).
    response_content_disposition : str, optional
        Override Content-Disposition header (e.g., "attachment; filename=report.pdf").
    response_content_type : str, optional
        Override Content-Type header for the download response.

    Returns
    -------
    PresignedUrlResult
        Contains the generated URL and metadata.

    Raises
    ------
    ClientError
        When URL generation fails (e.g., missing bucket permissions).
    """
    client = S3StorageClient(bucket=bucket).get_client()

    params = {
        "Bucket": bucket,
        "Key": key,
    }

    if response_content_disposition:
        params["ResponseContentDisposition"] = response_content_disposition
    if response_content_type:
        params["ResponseContentType"] = response_content_type

    url = client.generate_presigned_url(
        "get_object",
        Params=params,
        ExpiresIn=expires_in_seconds,
    )

    return PresignedUrlResult(
        url=url,
        bucket=bucket,
        key=key,
        expires_in_seconds=expires_in_seconds,
        http_method="GET",
    )
