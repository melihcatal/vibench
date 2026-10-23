import os
import json
from datetime import datetime, timezone

import boto3


def get_object_metadata(bucket: str, key: str, region_name: str | None = None) -> dict:
    session = boto3.session.Session(region_name=region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"))
    s3 = session.client("s3")
    response = s3.head_object(Bucket=bucket, Key=key)
    metadata = {
        "bucket": bucket,
        "key": key,
        "content_length": response.get("ContentLength"),
        "content_type": response.get("ContentType"),
        "etag": response.get("ETag"),
        "last_modified": response.get("LastModified").astimezone(timezone.utc).isoformat() if response.get("LastModified") else None,
        "storage_class": response.get("StorageClass"),
        "server_side_encryption": response.get("ServerSideEncryption"),
        "metadata": response.get("Metadata", {}),
    }
    return metadata


def main() -> None:
    bucket = os.environ["S3_BUCKET_NAME"]
    key = os.environ["S3_OBJECT_KEY"]
    region_name = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    print(json.dumps(get_object_metadata(bucket, key, region_name), sort_keys=True))


if __name__ == "__main__":
    main()
