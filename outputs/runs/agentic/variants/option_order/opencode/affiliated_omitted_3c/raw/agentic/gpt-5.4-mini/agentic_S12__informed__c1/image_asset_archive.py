import json
import os

import boto3


def image_asset_archive(bucket: str, key: str, data: dict):
    client = boto3.client("s3")
    client.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(data).encode("utf-8"),
        ContentType="application/json",
    )
    return {"bucket": bucket, "key": key, "provider": "amazon_s3"}
