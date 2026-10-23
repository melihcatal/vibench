import os
from dataclasses import dataclass
from typing import Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


@dataclass
class ObjectMetadata:
    bucket: str
    key: str
    etag: Optional[str]
    content_length: Optional[int]
    content_type: Optional[str]
    last_modified: Optional[str]
    storage_class: Optional[str]
    metadata: dict


def read_object_metadata(bucket: str, key: str, region_name: Optional[str] = None) -> ObjectMetadata:
    s3 = boto3.client("s3", region_name=region_name or os.environ.get("AWS_REGION"))
    response = s3.head_object(Bucket=bucket, Key=key)
    return ObjectMetadata(
        bucket=bucket,
        key=key,
        etag=response.get("ETag"),
        content_length=response.get("ContentLength"),
        content_type=response.get("ContentType"),
        last_modified=str(response.get("LastModified")) if response.get("LastModified") else None,
        storage_class=response.get("StorageClass"),
        metadata=response.get("Metadata", {}),
    )


def main() -> None:
    bucket = os.environ.get("S3_BUCKET")
    key = os.environ.get("S3_KEY")
    if not bucket or not key:
        raise SystemExit("S3_BUCKET and S3_KEY are required")
    try:
        result = read_object_metadata(bucket, key)
    except (ClientError, BotoCoreError) as exc:
        raise SystemExit(str(exc)) from exc
    print(result)


if __name__ == "__main__":
    main()
