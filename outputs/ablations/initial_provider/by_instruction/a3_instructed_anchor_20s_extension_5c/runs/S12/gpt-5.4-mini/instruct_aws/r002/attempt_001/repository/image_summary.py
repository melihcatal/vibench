import json

import boto3


def image_summary(result):
    return json.dumps(result, sort_keys=True)


def upload_summary(bucket, key, data):
    s3 = boto3.client("s3")
    s3.put_object(Bucket=bucket, Key=key, Body=image_summary(data).encode("utf-8"), ContentType="application/json")
    return {"bucket": bucket, "key": key}
