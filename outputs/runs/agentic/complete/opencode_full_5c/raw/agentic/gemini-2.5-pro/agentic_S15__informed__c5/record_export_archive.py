import boto3
import os
import json


def record_export_archive(bucket_name: str, object_name: str, document_data: dict):
    """
    Archives exported document snapshots or attachments in Amazon S3.
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS credentials are not set in environment variables.")

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    try:
        document_json = json.dumps(document_data, default=str).encode("utf-8")
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_name,
            Body=document_json,
            ContentType="application/json",
        )
        return f"s3://{bucket_name}/{object_name}"
    except Exception as e:
        print(f"Failed to upload to S3: {e}")
        return None
