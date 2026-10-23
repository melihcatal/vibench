from __future__ import annotations

import argparse
from typing import Optional

from storage_client import get_s3_client, handle_boto_error, load_storage_config
from storage_models import ObjectHeadResponse, isoformat_utc


def read_object_metadata(key: str, bucket: Optional[str] = None) -> ObjectHeadResponse:
    cfg = load_storage_config(bucket)
    client = get_s3_client(region=cfg.region, endpoint_url=cfg.endpoint_url, signature_version=cfg.signature_version)
    try:
        resp = client.head_object(Bucket=cfg.bucket, Key=key)
        return ObjectHeadResponse(
            bucket=cfg.bucket,
            key=key,
            etag=resp.get("ETag"),
            size=int(resp.get("ContentLength", 0)),
            last_modified=isoformat_utc(resp.get("LastModified")),
            content_type=resp.get("ContentType"),
            metadata=resp.get("Metadata", {}) or {},
        )
    except Exception as exc:
        raise handle_boto_error(exc)


def main() -> None:
    parser = argparse.ArgumentParser(description="Read S3 object metadata")
    parser.add_argument("key")
    parser.add_argument("--bucket")
    args = parser.parse_args()
    print(read_object_metadata(args.key, bucket=args.bucket))


if __name__ == "__main__":
    main()
