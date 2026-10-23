import os
import io
import json
import mimetypes
from datetime import datetime, timezone

import boto3


def archive_metrics_export(snapshot_path: str, bucket: str | None = None, key_prefix: str = "metrics-archives") -> dict:
    bucket_name = bucket or os.environ["AWS_S3_BUCKET"]
    s3 = boto3.client("s3")
    with open(snapshot_path, "rb") as f:
        data = f.read()
    basename = os.path.basename(snapshot_path)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    key = f"{key_prefix.rstrip('/')}/{timestamp}/{basename}"
    content_type = mimetypes.guess_type(snapshot_path)[0] or "application/octet-stream"
    s3.put_object(Bucket=bucket_name, Key=key, Body=data, ContentType=content_type)
    return {
        "provider": "aws_s3",
        "bucket": bucket_name,
        "key": key,
        "size_bytes": len(data),
        "archived_at": timestamp,
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_path")
    parser.add_argument("--bucket")
    parser.add_argument("--key-prefix", default="metrics-archives")
    args = parser.parse_args()
    result = archive_metrics_export(args.snapshot_path, bucket=args.bucket, key_prefix=args.key_prefix)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
