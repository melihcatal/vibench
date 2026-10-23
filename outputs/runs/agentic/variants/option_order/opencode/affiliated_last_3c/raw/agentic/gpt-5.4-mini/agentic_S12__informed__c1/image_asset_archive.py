import boto3


def image_asset_archive(bucket, key, body, content_type="text/plain"):
    s3 = boto3.client("s3")
    return s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType=content_type)
