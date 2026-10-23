import boto3

from vision_client import load_vision_config
from vision_models import normalize_archive_response


def image_asset_archive(payload, config=None):
    config = load_vision_config(config)
    client = boto3.client("s3")
    bucket = config["s3_bucket"]
    key = f"{config['s3_prefix'].rstrip('/')}/{payload.get('asset_name', 'image.json')}"
    response = client.put_object(Bucket=bucket, Key=key, Body=payload.get("content", b""), ContentType=payload.get("content_type", "application/json"))
    return normalize_archive_response({"uri": f"s3://{bucket}/{key}", "etag": response.get("ETag", ""), "content_type": payload.get("content_type", "application/json")})
