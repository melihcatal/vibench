from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional, Union

from storage_client import get_s3_client, handle_boto_error, load_storage_config
from storage_models import ObjectUploadRequest


def upload_object(key: str, source: Union[str, bytes, bytearray, memoryview], bucket: Optional[str] = None, content_type: Optional[str] = None, metadata: Optional[dict] = None):
    cfg = load_storage_config(bucket)
    client = get_s3_client(region=cfg.region, endpoint_url=cfg.endpoint_url, signature_version=cfg.signature_version)
    if isinstance(source, str):
        body = Path(source).read_bytes()
    else:
        body = bytes(source)
    req = ObjectUploadRequest(key=key, body=body, content_type=content_type, metadata=metadata)
    kwargs = {"Bucket": cfg.bucket, "Key": req.key, "Body": req.body}
    if req.content_type:
        kwargs["ContentType"] = req.content_type
    if req.metadata:
        kwargs["Metadata"] = req.metadata
    try:
        resp = client.put_object(**kwargs)
        return {"bucket": cfg.bucket, "key": req.key, "etag": resp.get("ETag")}
    except Exception as exc:
        raise handle_boto_error(exc)


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload an object to Amazon S3")
    parser.add_argument("key")
    parser.add_argument("source")
    parser.add_argument("--bucket")
    parser.add_argument("--content-type")
    args = parser.parse_args()
    print(upload_object(args.key, args.source, bucket=args.bucket, content_type=args.content_type))


if __name__ == "__main__":
    main()
