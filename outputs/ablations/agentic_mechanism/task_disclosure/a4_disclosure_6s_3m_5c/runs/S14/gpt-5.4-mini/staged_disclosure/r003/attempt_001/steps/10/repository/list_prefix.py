import argparse
import os
import sys

import boto3


def list_objects(bucket: str, prefix: str):
    client = boto3.client("s3")
    paginator = client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for item in page.get("Contents", []):
            yield item["Key"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("bucket")
    parser.add_argument("prefix", nargs="?", default="")
    args = parser.parse_args()

    bucket = args.bucket or os.environ.get("AWS_S3_BUCKET")
    prefix = args.prefix or os.environ.get("AWS_S3_PREFIX", "")

    if not bucket:
        print("bucket is required", file=sys.stderr)
        raise SystemExit(2)

    for key in list_objects(bucket, prefix):
        print(key)


if __name__ == "__main__":
    main()
