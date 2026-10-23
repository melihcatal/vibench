import boto3

from vision_client import get_vision_client
from vision_models import normalize_image_asset_archive


def image_asset_archive(payload, config=None):
    config = config or {}
    client = get_vision_client(config)
    s3_client = boto3.client("s3", region_name=config.get("region", "us-west-2"))
    bucket_name = config.get("bucket_name", "my-image-assets-bucket")
    key = f"{payload['image_id']}.jpg"
    s3_client.upload_fileobj(payload['image_bytes'], bucket_name, key)
    return normalize_image_asset_archive(bucket_name, key)