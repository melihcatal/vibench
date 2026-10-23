import boto3


def image_asset_archive(bucket, key, body):
    client = boto3.client("s3")
    client.put_object(Bucket=bucket, Key=key, Body=body)
    return {"bucket": bucket, "key": key}
