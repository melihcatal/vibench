import boto3


def image_asset_archive(payload, config=None):
    config = config or {}
    client = boto3.client("s3", region_name=config.get("region_name"))
    bucket = config["bucket"]
    key = config["key"]
    client.put_object(Bucket=bucket, Key=key, Body=payload["content"].encode("utf-8"), ContentType="text/plain")
    return {"bucket": bucket, "key": key}
