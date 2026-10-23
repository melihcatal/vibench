import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


@dataclass
class ObjectMetadataRequest:
    bucket: str
    key: str
    endpoint_url: Optional[str] = None
    region_name: Optional[str] = None


def _client(endpoint_url: Optional[str] = None, region_name: Optional[str] = None):
    return boto3.client(
        "s3",
        endpoint_url=endpoint_url or os.getenv("AWS_S3_ENDPOINT_URL"),
        region_name=region_name or os.getenv("AWS_REGION"),
    )


def read_object_metadata(bucket: str, key: str, endpoint_url: Optional[str] = None, region_name: Optional[str] = None) -> Dict[str, Any]:
    client = _client(endpoint_url=endpoint_url, region_name=region_name)
    response = client.head_object(Bucket=bucket, Key=key)
    metadata = {
        "bucket": bucket,
        "key": key,
        "content_length": response.get("ContentLength"),
        "content_type": response.get("ContentType"),
        "etag": response.get("ETag"),
        "last_modified": response.get("LastModified").isoformat() if response.get("LastModified") else None,
        "metadata": response.get("Metadata", {}),
        "storage_class": response.get("StorageClass"),
        "version_id": response.get("VersionId"),
    }
    return {k: v for k, v in metadata.items() if v is not None}


def read_object_metadata_from_request(request: ObjectMetadataRequest) -> Dict[str, Any]:
    return read_object_metadata(
        bucket=request.bucket,
        key=request.key,
        endpoint_url=request.endpoint_url,
        region_name=request.region_name,
    )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Read Amazon S3 object metadata")
    parser.add_argument("bucket")
    parser.add_argument("key")
    parser.add_argument("--endpoint-url")
    parser.add_argument("--region-name")
    args = parser.parse_args()
    try:
        result = read_object_metadata(args.bucket, args.key, args.endpoint_url, args.region_name)
        print(json.dumps(result, default=str))
    except (ClientError, BotoCoreError) as exc:
        raise SystemExit(str(exc))


if __name__ == "__main__":
    main()
