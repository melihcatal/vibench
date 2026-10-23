import boto3


def image_asset_archive(payload, config=None):
    config = config or {}
    s3_client = boto3.client('s3', region_name=config.get('region'))
    bucket_name = config.get('bucket_name')
    key = f"{payload['image_id']}.jpg"
    s3_client.upload_fileobj(
        payload['image_bytes'],
        bucket_name,
        key,
        ExtraArgs={"ContentType": "image/jpeg"}
    )
    return {'archive_location': f"s3://{bucket_name}/{key}"}