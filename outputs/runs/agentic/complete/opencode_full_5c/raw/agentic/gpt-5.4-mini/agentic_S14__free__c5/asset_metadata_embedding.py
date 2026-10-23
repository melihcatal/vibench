import os

import boto3

from storage_client import bucket_name, client


def asset_metadata_embedding(bucket: str | None, key: str):
    s3 = client()
    bedrock = boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
    )
    head = s3.head_object(Bucket=bucket_name(bucket), Key=key)
    text = (
        s3.get_object(Bucket=bucket_name(bucket), Key=key)["Body"]
        .read()
        .decode("utf-8", errors="ignore")
    )
    payload = {"inputText": f"{key}\n{head.get('ContentType', '')}\n{text}"}
    return bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body=(str(payload).replace("'", '"')).encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
