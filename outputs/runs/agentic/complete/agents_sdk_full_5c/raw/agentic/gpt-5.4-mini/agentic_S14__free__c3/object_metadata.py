from __future__ import annotations

import argparse

from storage_client import get_s3_client, load_settings
from storage_models import MetadataResponse


def read_object_metadata(bucket: str, key: str, version_id: str | None = None) -> MetadataResponse:
    s3 = get_s3_client()
    kwargs = {"Bucket": bucket, "Key": key}
    if version_id:
        kwargs["VersionId"] = version_id
    response = s3.head_object(**kwargs)
    return MetadataResponse(
        bucket=bucket,
        key=key,
        size=response.get("ContentLength"),
        content_type=response.get("ContentType"),
        last_modified=response.get("LastModified").isoformat() if response.get("LastModified") else None,
        etag=response.get("ETag"),
        metadata=response.get("Metadata", {}),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bucket")
    parser.add_argument("key")
    args = parser.parse_args()
    settings = load_settings()
    print(read_object_metadata(args.bucket or settings.bucket_name, args.key))
