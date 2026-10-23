import boto3

from vision_client import load_config


def image_asset_archive(payload, config=None):
    cfg = load_config(config)
    client = boto3.client("s3", region_name=cfg.get("region"))
    bucket = cfg.get("bucket")
    key = cfg.get("key", "image-analysis/artifact.json")
    if bucket:
        client.put_object(Bucket=bucket, Key=key, Body=str(payload).encode("utf-8"))
    return {"bucket": bucket, "key": key, "stored": bool(bucket)}
