from boto3 import client


def image_asset_archive(
    bucket: str, key: str, body: bytes, content_type: str = "application/json"
):
    s3 = client("s3")
    s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType=content_type)
    return {"bucket": bucket, "key": key}
