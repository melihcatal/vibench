import os
import datetime
from storage_client import StorageClient, DownloadPresignRequest
from storage_models import DownloadPresignRequest

# Explicit provider identification (IBM Cloud Object Storage)
PROVIDER = "IBM Cloud Object Storage"


class PresignError(Exception):
    """Raised when URL generation fails."""

    pass


def presign_download(bucket_name: str, key: str, expires_in_seconds: int = 3600) -> str:
    """
    Create a time‑limited signed URL for downloading an object.

    Args:
        bucket_name (str): Bucket containing the object.
        key (str): Object path.
        expires_in_seconds (int): How long the URL remains valid.
    Returns:
        str: Signed URL.
    """
    req = DownloadPresignRequest(
        bucket_name=bucket_name, key=key, expires_in_seconds=expires_in_seconds
    )
    url = client.get_presigned_url(req.bucket_name, req.key, req.expires_in_seconds)
    if not url.startswith("https://"):
        raise PresignError(f"Invalid URL returned from {PROVIDER}: {url}")
    print(
        f"[{PROVIDER}] Presigned URL for {bucket_name}/{key} (expires in {expires_in_seconds}s): {url}"
    )
    return url


# Simple helper to parse an expiration string into seconds
parse_expiration = lambda s: (
    int(
        datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").timestamp()
        - datetime.datetime.utcnow().timestamp()
    )
    if s
    else 3600
)

# If run as script, accept CLI arguments
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print(
            "Usage: presigned_download.py <bucket> <key> <expires-seconds-or-iso> (optional)"
        )
        sys.exit(1)
    bucket = sys.argv[1]
    key = sys.argv[2]
    expires = sys.argv[3]
    url = presign_download(
        bucket, key, expires_in_seconds=(parse_expiration(expires) if expires else 3600)
    )
    print(url)
