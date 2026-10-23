from __future__ import annotations

import argparse
from datetime import timedelta

from storage_client import get_s3_client, load_settings


def create_presigned_download_url(bucket: str, key: str, expires_in: int = 900, version_id: str | None = None) -> str:
    s3 = get_s3_client()
    params = {"Bucket": bucket, "Key": key}
    if version_id:
        params["VersionId"] = version_id
    return s3.generate_presigned_url("get_object", Params=params, ExpiresIn=expires_in)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bucket")
    parser.add_argument("key")
    parser.add_argument("--expires-in", type=int, default=900)
    args = parser.parse_args()
    settings = load_settings()
    print(create_presigned_download_url(args.bucket or settings.bucket_name, args.key, args.expires_in))
