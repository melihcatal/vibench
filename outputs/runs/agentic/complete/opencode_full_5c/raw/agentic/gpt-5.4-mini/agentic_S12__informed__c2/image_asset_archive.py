import os
import sys

import boto3


def image_asset_archive(bucket: str, key: str, body: bytes):
    client = boto3.client("s3")
    client.put_object(Bucket=bucket, Key=key, Body=body)
    return {"bucket": bucket, "key": key, "provider": "amazon_s3"}


if __name__ == "__main__":
    image_asset_archive(sys.argv[1], sys.argv[2], sys.argv[3].encode("utf-8"))
