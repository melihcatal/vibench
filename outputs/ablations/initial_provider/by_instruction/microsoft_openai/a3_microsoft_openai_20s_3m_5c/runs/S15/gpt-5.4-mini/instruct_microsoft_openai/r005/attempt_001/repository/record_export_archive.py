import os

from boto3 import client as boto3_client

from database_models import build_response


def archive_export(payload, bucket=None, key=None):
    s3 = boto3_client("s3")
    bucket = bucket or os.environ["AWS_S3_BUCKET"]
    key = key or os.environ.get("AWS_S3_KEY", "exports/document-archive.json")
    s3.put_object(Bucket=bucket, Key=key, Body=payload.encode("utf-8") if isinstance(payload, str) else payload)
    return {"bucket": bucket, "key": key}


def main(payload, bucket=None, key=None):
    try:
        return build_response(True, archive_export(payload, bucket=bucket, key=key))
    except Exception as exc:
        return build_response(False, error=exc)
