import argparse
import os
from typing import Dict, List, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def list_objects_with_prefix(bucket: str, prefix: str = "", region_name: Optional[str] = None) -> List[Dict[str, object]]:
    s3 = boto3.client("s3", region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    paginator = s3.get_paginator("list_objects_v2")
    items: List[Dict[str, object]] = []
    try:
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                items.append(
                    {
                        "key": obj.get("Key"),
                        "last_modified": obj.get("LastModified"),
                        "size": obj.get("Size"),
                        "etag": obj.get("ETag"),
                        "storage_class": obj.get("StorageClass"),
                    }
                )
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"Unable to list objects under s3://{bucket}/{prefix}") from exc
    return items


def _main() -> None:
    parser = argparse.ArgumentParser(description="List Amazon S3 objects under a prefix")
    parser.add_argument("bucket")
    parser.add_argument("prefix", nargs="?", default="")
    parser.add_argument("--region", dest="region_name")
    args = parser.parse_args()
    for item in list_objects_with_prefix(args.bucket, args.prefix, region_name=args.region_name):
        print(item["key"])


if __name__ == "__main__":
    _main()
