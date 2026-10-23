from typing import Dict

import boto3


def image_asset_archive(bucket: str, key: str, data: bytes, content_type: str = "application/json") -> Dict[str, str]:
    client = boto3.client("s3")
    client.put_object(Bucket=bucket, Key=key, Body=data, ContentType=content_type)
    return {"provider": "aws.s3", "bucket": bucket, "key": key}
