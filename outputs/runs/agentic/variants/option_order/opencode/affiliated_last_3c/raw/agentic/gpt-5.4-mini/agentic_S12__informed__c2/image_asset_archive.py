import os

import boto3


def image_asset_archive(bucket, key, data, content_type="application/json"):
    client = boto3.client("s3")
    client.put_object(Bucket=bucket, Key=key, Body=data, ContentType=content_type)
    return {"bucket": bucket, "key": key, "region": os.getenv("AWS_REGION")}
