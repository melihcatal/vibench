import os

import boto3


def main(bucket: str, key: str, body: bytes):
    return boto3.client("s3").put_object(Bucket=bucket, Key=key, Body=body, ServerSideEncryption=os.getenv("S3_SSE", "AES256"))
