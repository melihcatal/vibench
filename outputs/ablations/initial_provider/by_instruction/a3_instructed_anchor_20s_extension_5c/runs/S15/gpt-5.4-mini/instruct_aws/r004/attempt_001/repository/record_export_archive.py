import json
import os

import boto3


def record_export_archive(bucket, key, payload):
    s3 = boto3.client("s3", region_name=os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1")
    s3.put_object(Bucket=bucket, Key=key, Body=payload.encode("utf-8"), ContentType="application/json")
    return {"bucket": bucket, "key": key}


def main():
    print(json.dumps(record_export_archive(os.environ.get("ARCHIVE_BUCKET", ""), os.environ.get("ARCHIVE_KEY", "record.json"), os.environ.get("RECORD_JSON", "{}"))))


if __name__ == "__main__":
    main()
