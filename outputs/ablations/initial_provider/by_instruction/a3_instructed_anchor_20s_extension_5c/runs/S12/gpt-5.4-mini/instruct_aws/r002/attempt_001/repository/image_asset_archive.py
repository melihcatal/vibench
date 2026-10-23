import os
import json

import boto3


def image_asset_archive(bucket, key, artifacts):
    s3 = boto3.client("s3")
    s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(artifacts).encode("utf-8"), ContentType="application/json")
    return {"bucket": bucket, "key": key, "region": os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")}
