import os
import sys

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def list_objects(bucket: str, prefix: str = "") -> int:
    s3 = boto3.client("s3")
    paginator = s3.get_paginator("list_objects_v2")
    found = False

    try:
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                found = True
                print(obj["Key"])
    except (BotoCoreError, ClientError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    return 0 if found else 0


def main() -> int:
    bucket = os.environ.get("AWS_S3_BUCKET")
    prefix = os.environ.get("AWS_S3_PREFIX", "")

    if not bucket:
        print("AWS_S3_BUCKET is required", file=sys.stderr)
        return 2

    return list_objects(bucket, prefix)


if __name__ == "__main__":
    raise SystemExit(main())
