import boto3

from vision_client import load_config


def image_asset_archive(payload, config=None):
    config = load_config(config)
    client = boto3.client("s3", region_name=config.get("region"))
    bucket = config.get("bucket")
    key = payload.get("key", "image-analysis.json") if isinstance(payload, dict) else "image-analysis.json"
    body = payload.get("body", b"") if isinstance(payload, dict) else b""
    client.put_object(Bucket=bucket, Key=key, Body=body)
    return {"bucket": bucket, "key": key}
