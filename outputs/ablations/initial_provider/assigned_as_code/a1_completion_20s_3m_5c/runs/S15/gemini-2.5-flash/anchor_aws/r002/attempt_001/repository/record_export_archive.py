import os

import boto3


def archive_document_snapshot(file_content, bucket_name, object_key):
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    s3_client = boto3.client("s3", region_name=region_name)

    try:
        s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=file_content)
        return {
            "message": f"Successfully archived {object_key} to s3://{bucket_name}",
            "bucket": bucket_name,
            "object_key": object_key,
            "provider": "AWS S3",
        }
    except Exception as e:
        return {"error": str(e), "provider": "AWS S3"}
