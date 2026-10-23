import json

import boto3

from storage_client import get_s3_client, get_storage_config


bedrock_runtime = boto3.client("bedrock-runtime", region_name=get_storage_config().region_name)


def embed_asset_metadata(bucket: str, key: str) -> dict:
    s3 = get_s3_client(get_storage_config())
    head = s3.head_object(Bucket=bucket, Key=key)
    obj = s3.get_object(Bucket=bucket, Key=key)
    text = obj["Body"].read().decode("utf-8", errors="ignore")
    payload_text = json.dumps({"metadata": head.get("Metadata", {}), "content": text[:6000]})
    response = bedrock_runtime.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps({"inputText": payload_text}),
        accept="application/json",
        contentType="application/json",
    )
    return response