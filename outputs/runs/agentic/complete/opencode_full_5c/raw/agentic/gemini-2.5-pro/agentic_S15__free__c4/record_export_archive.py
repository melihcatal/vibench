import os
import boto3
import json


def record_export_archive(document_id: str, document_data: dict):
    bucket_name = os.environ.get("S3_ARCHIVE_BUCKET")
    if not bucket_name:
        raise ValueError("S3_ARCHIVE_BUCKET environment variable not set.")

    s3_client = boto3.client("s3")

    file_key = f"export/{document_id}.json"

    s3_client.put_object(
        Bucket=bucket_name,
        Key=file_key,
        Body=json.dumps(document_data, indent=2),
        ContentType="application/json",
    )

    return f"s3://{bucket_name}/{file_key}"
