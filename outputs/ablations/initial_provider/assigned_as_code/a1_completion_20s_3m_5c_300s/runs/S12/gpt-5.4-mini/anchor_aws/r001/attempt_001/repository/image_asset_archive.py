import boto3

from vision_client import load_vision_config


def image_asset_archive(payload, config=None):
    config = load_vision_config(config)
    client = boto3.client("s3", region_name=config.get("region"))
    client.put_object(
        Bucket=payload["bucket"],
        Key=payload["key"],
        Body=payload.get("body", b""),
        ContentType=payload.get("content_type", "application/json"),
    )
    return {"bucket": payload["bucket"], "key": payload["key"]}
