import os

import boto3


s3 = boto3.client("s3")


def image_asset_archive(bucket, key, content):
    s3.put_object(Bucket=bucket, Key=key, Body=content.encode("utf-8"), ContentType="text/plain")
    return {"bucket": bucket, "key": key, "status": "archived"}
