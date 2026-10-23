import os
import boto3


def image_asset_archive(bucket_name, object_key, file_path):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    s3_client.upload_file(file_path, bucket_name, object_key)
