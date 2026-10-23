import os
import boto3
import json

def archive_document_snapshot(document_id: str, document_data: dict, bucket_key_prefix: str = "document_archives/") -> str:
    region = os.environ.get("AWS_REGION")
    bucket_name = os.environ.get("AWS_S3_BUCKET_NAME")

    if not region:
        raise ValueError("AWS_REGION environment variable not set.")
    if not bucket_name:
        raise ValueError("AWS_S3_BUCKET_NAME environment variable not set.")

    s3_client = boto3.client("s3", region_name=region)

    file_content = json.dumps(document_data, indent=2)
    object_key = f"{bucket_key_prefix}{document_id}-{os.urandom(4).hex()}.json"

    s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=file_content.encode('utf-8'),
        ContentType='application/json'
    )
    return f"s3://{bucket_name}/{object_key}"
