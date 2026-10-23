import os
import boto3
import json


def image_asset_archive(image_path: str, artifacts: dict, bucket_name: str) -> str:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    key = f"image_analysis/{os.path.splitext(os.path.basename(image_path))[0]}_artifacts.json"
    s3_client.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(artifacts))
    return f"s3://{bucket_name}/{key}"
