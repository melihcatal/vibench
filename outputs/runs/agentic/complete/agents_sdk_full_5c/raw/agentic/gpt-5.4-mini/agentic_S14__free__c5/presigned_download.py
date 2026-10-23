from __future__ import annotations

import argparse
from typing import Optional

from storage_client import get_s3_client, handle_boto_error, load_storage_config
from storage_models import PresignedDownloadResponse


def create_presigned_download_url(key: str, expires_in: int = 900, bucket: Optional[str] = None) -> PresignedDownloadResponse:
    cfg = load_storage_config(bucket)
    client = get_s3_client(region=cfg.region, endpoint_url=cfg.endpoint_url, signature_version=cfg.signature_version)
    try:
        url = client.generate_presigned_url(
            "get_object",
            Params={"Bucket": cfg.bucket, "Key": key},
            ExpiresIn=expires_in,
        )
        return PresignedDownloadResponse(bucket=cfg.bucket, key=key, url=url, expires_in=expires_in)
    except Exception as exc:
        raise handle_boto_error(exc)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a presigned S3 download URL")
    parser.add_argument("key")
    parser.add_argument("--bucket")
    parser.add_argument("--expires-in", type=int, default=900)
    args = parser.parse_args()
    print(create_presigned_download_url(args.key, expires_in=args.expires_in, bucket=args.bucket))


if __name__ == "__main__":
    main()
