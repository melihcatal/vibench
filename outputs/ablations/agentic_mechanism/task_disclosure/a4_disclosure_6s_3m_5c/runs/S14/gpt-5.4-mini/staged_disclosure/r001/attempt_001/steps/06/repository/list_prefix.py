import argparse
import json
import os
import sys

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def list_objects(bucket, prefix, region=None):
    session = boto3.session.Session(region_name=region or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    client = session.client("s3")
    paginator = client.get_paginator("list_objects_v2")
    objects = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for item in page.get("Contents", []):
            objects.append(
                {
                    "key": item["Key"],
                    "size": item["Size"],
                    "last_modified": item["LastModified"].isoformat(),
                    "etag": item.get("ETag", ""),
                }
            )
    return objects


def main(argv=None):
    parser = argparse.ArgumentParser(description="List Amazon S3 objects under a prefix")
    parser.add_argument("bucket")
    parser.add_argument("prefix")
    parser.add_argument("--region")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        objects = list_objects(args.bucket, args.prefix, args.region)
    except (ClientError, BotoCoreError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(objects, indent=2))
    else:
        for obj in objects:
            print(obj["key"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
