import boto3
import os


def record_export_archive(file_content: bytes, bucket_name: str, object_name: str) -> dict:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION"),
    )

    response = s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=file_content)
    return {"ETag": response["ETag"], "VersionId": response.get("VersionId")}
