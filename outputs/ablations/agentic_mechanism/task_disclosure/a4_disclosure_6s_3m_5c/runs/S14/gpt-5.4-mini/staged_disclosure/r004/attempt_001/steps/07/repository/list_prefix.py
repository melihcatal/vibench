import os
import sys
import boto3


def list_objects_with_prefix(bucket, prefix):
    s3 = boto3.client("s3")
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for item in page.get("Contents", []):
            print(item["Key"])


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: list_prefix.py BUCKET PREFIX")
    bucket = sys.argv[1]
    prefix = sys.argv[2]
    if not bucket:
        bucket = os.environ["AWS_S3_BUCKET"]
    list_objects_with_prefix(bucket, prefix)


if __name__ == "__main__":
    main()
