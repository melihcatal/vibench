import os

import boto3


def archive_record(bucket, key, content):
    client = boto3.client("s3")
    client.put_object(
        Bucket=bucket,
        Key=key,
        Body=content.encode("utf-8"),
        ContentType="application/json",
    )
    return {"bucket": bucket, "key": key, "region": os.getenv("AWS_REGION")}
