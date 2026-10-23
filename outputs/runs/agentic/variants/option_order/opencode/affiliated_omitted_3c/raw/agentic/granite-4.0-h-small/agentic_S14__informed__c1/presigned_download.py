import os
import boto3
from .storage_client import StorageClient


class PresignedDownload:
    """Create a time‑limited signed URL for downloading an object stored in S3."""

    @classmethod
    def sign(cls, bucket_name: str, key: str, expires_sec: int = 3600):
        url = StorageClient.generate_presigned_url(
            Bucket=bucket_name,
            Key=key,
            ExpiresIn=expires_sec,
        )
        return {
            "status": "signed_url_created",
            "bucket": bucket_name,
            "key": key,
            "url": url,
            "expires_in_seconds": expires_sec,
        }
