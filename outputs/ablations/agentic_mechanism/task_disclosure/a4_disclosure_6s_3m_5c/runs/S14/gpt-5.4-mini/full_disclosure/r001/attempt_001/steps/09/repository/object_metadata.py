import os
from typing import Any, Dict, Optional

import boto3


def _require_env(name: str, fallback: Optional[str] = None) -> str:
    value = os.environ.get(name, fallback)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def get_object_metadata(bucket: str, key: str, region_name: Optional[str] = None) -> Dict[str, Any]:
    session = boto3.session.Session(region_name=region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"))
    client = session.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
    )
    response = client.head_object(Bucket=bucket, Key=key)
    metadata = dict(response.get("Metadata", {}))
    return {
        "bucket": bucket,
        "key": key,
        "etag": response.get("ETag"),
        "content_length": response.get("ContentLength"),
        "content_type": response.get("ContentType"),
        "last_modified": response.get("LastModified"),
        "storage_class": response.get("StorageClass"),
        "version_id": response.get("VersionId"),
        "server_side_encryption": response.get("ServerSideEncryption"),
        "metadata": metadata,
        "raw": response,
    }


def main() -> None:
    bucket = _require_env("OBJECT_STORAGE_BUCKET")
    key = _require_env("OBJECT_STORAGE_KEY")
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    result = get_object_metadata(bucket=bucket, key=key, region_name=region)
    print(result)


if __name__ == "__main__":
    main()
