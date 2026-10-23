import os

import boto3


def image_bytes(source):
    if source is None:
        raise ValueError("source is required")
    if isinstance(source, (bytes, bytearray)):
        return bytes(source)
    if isinstance(source, str):
        if source.startswith("s3://"):
            bucket, key = source[5:].split("/", 1)
            s3 = boto3.client("s3")
            return s3.get_object(Bucket=bucket, Key=key)["Body"].read()
        with open(source, "rb") as f:
            return f.read()
    raise TypeError("unsupported image source")


def rekognition_client():
    return boto3.client("rekognition", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))


def s3_client():
    return boto3.client("s3", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
