import os
import sys
import boto3
from botocore.exceptions import ClientError


def head_object(bucket: str, key: str, region: str | None = None) -> dict:
    session = boto3.session.Session(region_name=region or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    client = session.client("s3")
    return client.head_object(Bucket=bucket, Key=key)


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: object_metadata.py <bucket> <key> [region]", file=sys.stderr)
        return 2

    bucket = sys.argv[1]
    key = sys.argv[2]
    region = sys.argv[3] if len(sys.argv) > 3 else None

    try:
        metadata = head_object(bucket, key, region)
    except ClientError as exc:
        print(exc, file=sys.stderr)
        return 1

    for field in (
        "ContentLength",
        "ContentType",
        "ETag",
        "LastModified",
        "StorageClass",
        "ChecksumCRC32",
        "ChecksumCRC32C",
        "ChecksumSHA1",
        "ChecksumSHA256",
    ):
        if field in metadata:
            print(f"{field}: {metadata[field]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
