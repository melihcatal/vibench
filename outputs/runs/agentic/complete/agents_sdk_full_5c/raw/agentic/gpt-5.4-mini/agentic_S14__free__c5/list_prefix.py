from __future__ import annotations

import argparse
from typing import List, Optional

from storage_client import get_s3_client, handle_boto_error, load_storage_config
from storage_models import ListedObject, isoformat_utc


def list_objects_with_prefix(prefix: str = "", bucket: Optional[str] = None, max_keys: int = 1000) -> List[ListedObject]:
    cfg = load_storage_config(bucket)
    client = get_s3_client(region=cfg.region, endpoint_url=cfg.endpoint_url, signature_version=cfg.signature_version)
    try:
        resp = client.list_objects_v2(Bucket=cfg.bucket, Prefix=prefix, MaxKeys=max_keys)
        results: List[ListedObject] = []
        for item in resp.get("Contents", []) or []:
            results.append(
                ListedObject(
                    key=item["Key"],
                    size=int(item.get("Size", 0)),
                    last_modified=isoformat_utc(item.get("LastModified")),
                    etag=item.get("ETag"),
                    storage_class=item.get("StorageClass"),
                )
            )
        return results
    except Exception as exc:
        raise handle_boto_error(exc)


def main() -> None:
    parser = argparse.ArgumentParser(description="List S3 objects by prefix")
    parser.add_argument("--bucket")
    parser.add_argument("--prefix", default="")
    parser.add_argument("--max-keys", type=int, default=1000)
    args = parser.parse_args()
    print(list_objects_with_prefix(prefix=args.prefix, bucket=args.bucket, max_keys=args.max_keys))


if __name__ == "__main__":
    main()
