import boto3


def image_asset_archive(image_bytes, caption, config=None):
    config = config or {}
    client = boto3.client("s3", region_name=config.get("region"))
    client.put_object(
        Bucket=config.get("bucket"),
        Key=f"images/{caption}.jpg",
        Body=image_bytes,
    )