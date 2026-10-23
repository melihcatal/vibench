import json

import boto3


def image_asset_archive(bucket: str, key: str, artifact):
    s3 = boto3.client("s3")
    body = json.dumps(artifact).encode("utf-8")
    s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json")
    return {"bucket": bucket, "key": key}
