import os
import json
import boto3


def image_asset_archive(bucket, key_prefix, analysis):
    s3 = boto3.client("s3")
    body = json.dumps(analysis).encode("utf-8")
    key = f"{key_prefix.rstrip('/')}/analysis.json"
    s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json")
    return {"bucket": bucket, "key": key, "bytes": len(body)}
