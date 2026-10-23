import json
import os
import sys

import boto3


def record_export_archive(record: dict, archive_key: str):
    client = boto3.client("s3", region_name=os.getenv("AWS_REGION", "us-east-1"))
    bucket = os.environ["S3_ARCHIVE_BUCKET"]
    body = json.dumps(record, default=str).encode("utf-8")
    client.put_object(
        Bucket=bucket, Key=archive_key, Body=body, ContentType="application/json"
    )
    return {"bucket": bucket, "key": archive_key}


def main() -> None:
    payload = json.loads(sys.stdin.read())
    result = record_export_archive(dict(payload["record"]), payload["archive_key"])
    sys.stdout.write(json.dumps(result, default=str))


if __name__ == "__main__":
    main()
