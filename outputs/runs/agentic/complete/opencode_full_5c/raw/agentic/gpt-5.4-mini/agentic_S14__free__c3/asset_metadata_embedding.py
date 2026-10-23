import json
import os

import boto3

from storage_client import get_s3_client


def asset_metadata_embedding(bucket: str, key: str):
    s3 = get_s3_client()
    head = s3.head_object(Bucket=bucket, Key=key)
    obj = s3.get_object(Bucket=bucket, Key=key)
    text = obj["Body"].read().decode("utf-8", errors="ignore")
    bedrock = boto3.client(
        "bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1")
    )
    payload = {
        "inputText": json.dumps(
            {"metadata": head.get("Metadata", {}), "text": text[:4000]}
        ),
    }
    return bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v1", body=json.dumps(payload)
    )
