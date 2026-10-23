import json
from boto3 import client as boto3_client


def image_asset_archive(bucket, key, payload):
    s3 = boto3_client("s3")
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(payload).encode("utf-8"),
        ContentType="application/json",
    )
    return {"bucket": bucket, "key": key}
